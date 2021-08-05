# -*- coding: utf-8 -*-

# This file is part of the FlOpEDT/FlOpScheduler project.
# Copyright (c) 2017
# Authors: Iulian Ober, Paul Renaud-Goud, Pablo Seban, et al.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program. If not, see
# <http://www.gnu.org/licenses/>.
#
# You can be released from the requirements of the license by purchasing
# a commercial license. Buying such a license is mandatory as soon as
# you develop activities involving the FlOpEDT/FlOpScheduler software
# without disclosing the source code of your own applications.


from FlOpEDT.decorators import timer
from base.partition import Partition
from datetime import timedelta

from django.http.response import JsonResponse
from TTapp.TTConstraints.no_course_constraints import NoTutorCourseOnDay
from base.models import CourseStartTimeConstraint, Dependency, ModulePossibleTutors, UserPreference
from django.contrib.postgres.fields import ArrayField

from django.db import models
from django.db.models import Q
from base.timing import TimeInterval, flopdate_to_datetime, french_format, Day

from TTapp.ilp_constraints.constraint_type import ConstraintType
from TTapp.ilp_constraints.constraint import Constraint
from TTapp.slots import days_filter, slots_filter
from TTapp.TTConstraint import TTConstraint
from TTapp.ilp_constraints.constraints.dependencyConstraint import DependencyConstraint
from django.utils.translation import gettext as _

class SimultaneousCourses(TTConstraint):
    """
    Force courses to start simultaneously
    """
    courses = models.ManyToManyField('base.Course', related_name='simultaneous_courses_constraints')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        courses_weeks_and_years = set((c.week, c.year) for c in self.courses.all())
        nb = len(courses_weeks_and_years)
        if nb == 0:
            return
        elif nb > 1:
            self.delete()
            raise Exception("Simultaneous courses need to have the same week: not saved")
        else:
            week, year = courses_weeks_and_years.pop()
            self.week = week
            self.year = year
            super().save(*args, **kwargs)

    @classmethod
    def get_viewmodel_prefetch_attributes(cls):
        attributes = super().get_viewmodel_prefetch_attributes()
        attributes.extend(['courses'])
        return attributes

    def enrich_model(self, ttmodel, week, ponderation=1):
        course_types = set(c.type for c in self.courses.all())
        relevant_courses = list(c for c in self.courses.all() if c.week in ttmodel.weeks)
        nb_courses = len(relevant_courses)
        if nb_courses < 2:
            return
        possible_start_times = set()
        for t in course_types:
            possible_start_times |= set(t.coursestarttimeconstraint_set.all()[0].allowed_start_times)
        for day in days_filter(ttmodel.wdb.days, week=week):
            for st in possible_start_times:
                check_var = ttmodel.add_var("check_var")
                expr = ttmodel.lin_expr()
                for c in relevant_courses:
                    possible_slots = slots_filter(ttmodel.wdb.compatible_slots[c], start_time=st, day=day)
                    for sl in possible_slots:
                        expr += ttmodel.TT[(sl, c)]
                ttmodel.add_constraint(nb_courses * check_var - expr, '==', 0,
                                       Constraint(constraint_type=ConstraintType.SIMULTANEOUS_COURSES,
                                                  courses=relevant_courses))
                ttmodel.add_constraint(expr - check_var, '>=', 0,
                                       Constraint(constraint_type=ConstraintType.SIMULTANEOUS_COURSES,
                                       courses=relevant_courses))

    def get_viewmodel(self):
        view_model = super().get_viewmodel()
        details = view_model['details']

        if self.courses.exists():
            details.update({'courses': ', '.join([str(course) for course in self.courses.all()])})

        return view_model

    def one_line_description(self):
        return f"Les cours {self.courses.all()} doivent être simultanés !"

    class Meta:
        verbose_name_plural = "Simultaneous courses"


class LimitedStartTimeChoices(TTConstraint):
    """
    Limit the possible start times
    """

    module = models.ForeignKey('base.Module',
                               null=True,
                               blank=True,
                               default=None,
                               on_delete=models.CASCADE)
    tutor = models.ForeignKey('people.Tutor',
                              null=True,
                              blank=True,
                              default=None,
                              on_delete=models.CASCADE)
    group = models.ForeignKey('base.StructuralGroup',
                              null=True,
                              blank=True,
                              default=None,
                              on_delete=models.CASCADE)
    course_type = models.ForeignKey('base.CourseType',
                                    null=True,
                                    blank=True,
                                    default=None,
                                    on_delete=models.CASCADE)
    possible_week_days = ArrayField(models.CharField(max_length=2, choices=Day.CHOICES), blank=True, null=True)
    possible_start_times = ArrayField(models.PositiveSmallIntegerField())

    def enrich_model(self, ttmodel, week, ponderation=1.):
        fc = self.get_courses_queryset_by_attributes(ttmodel, week)
        pst = self.possible_start_times
        if self.possible_week_days is None:
            pwd = list(c[0] for c in Day.CHOICES)
        else:
            pwd = self.possible_week_days
        if self.tutor is None:
            relevant_sum = ttmodel.sum(ttmodel.TT[(sl, c)]
                                       for c in fc
                                       for sl in ttmodel.wdb.compatible_slots[c] if (sl.start_time not in pst or
                                                                                     sl.day.day not in pwd))
        else:
            relevant_sum = ttmodel.sum(ttmodel.TTinstructors[(sl, c, self.tutor)]
                                       for c in fc
                                       for sl in ttmodel.wdb.compatible_slots[c] if (sl.start_time not in pst or
                                                                                     sl.day.day not in pwd))
        if self.weight is not None:
            ttmodel.add_to_generic_cost(self.local_weight() * ponderation * relevant_sum, week=week)
        else:
            ttmodel.add_constraint(relevant_sum, '==', 0,
                                   Constraint(constraint_type=ConstraintType.LIMITED_START_TIME_CHOICES,
                                              instructors=self.tutor, groups=self.group, modules=self.module,))

    def one_line_description(self):
        text = "Les "
        if self.course_type:
            text += str(self.course_type)
        else:
            text += "cours"
        if self.module:
            text += " de " + str(self.module)
        if self.tutor:
            text += ' de ' + str(self.tutor)
        if self.train_progs.exists():
            text += ' en ' + ', '.join([train_prog.abbrev for train_prog in self.train_progs.all()])
        else:
            text += " pour toutes les promos."
        if self.group:
            text += ' avec le groupe ' + str(self.group)
        text += " ne peuvent avoir lieu qu'à "
        for pst in self.possible_start_times:
            text += french_format(pst) + ', '
        return text

################    ConsiderDependencies FUNCTIONS      ################
def find_successive_slots(course_slot1, course_slot2, course1_duration, course2_duration):
    '''This function returns True if it finds a slot for the second course right after one of the first one with enough
    time duration.
    Complexity on O(n^2): n being the number of slots for each course.
    
    Parameters:
        course_slot1 (list(TimeInterval)): A list of time interval representing when the first course can be placed
        course_slot2 (list(TimeInterval)): A list of time interval representing when the second course can be placed
        course1_duration (timedelta): The duration of the first course
        course2_duration (timedelta): The duration of the second course
        
    Returns:
        (boolean): If we found at least one eligible slot'''
    for cs1 in course_slot1:
        possible_start_time = cs1.start + course1_duration
        for cs2 in course_slot2:
            if cs2.start <= cs1.end:
                if cs2.start > possible_start_time and cs2.end >= cs2.start + course2_duration:
                    return True
                elif cs2.start <= possible_start_time and cs2.end >= possible_start_time + course2_duration:
                    return True
            if cs2.start > possible_start_time:
                break
    return False


def find_day_gap_slots(course_slots1, course_slots2, day_gap):
    """This function search in the available times for each course if we can find a slot for the second course after a day gap passed
    in the parameters.
    
    Parameters:
        course_slots1 (list(TimeInterval)): The TimeIntervals (starting datetime and ending datetime) available for the first course
        course_slots2 (list(TimeInterval)): The TimeIntervals (starting datetime and ending datetime) available for the second course
        day_gap (int): The number of days between the two courses

    Returns:
        (boolean) : whether there is available time for the second course after the day gap or not"""
    day_slot = course_slots1[0].start + timedelta(days=day_gap) - timedelta(hours=course_slots1[0].start.hour, minutes=course_slots1[0].start.minute)
    for cs2 in course_slots2:
        if cs2.start > day_slot:
            return True
    return False

class ConsiderDependencies(TTConstraint):
    """
    Transform the constraints of dependency saved on the DB in model constraints:
    -include dependencies and successiveness
    -include non same-day constraint
    -include simultaneity (double dependency)
    If there is a weight, it's a preference, else it's a constraint...
    """
    modules = models.ManyToManyField('base.Module', blank=True)

    @timer
    def pre_analyse(self, week):
        """Pre analysis of the Constraint
        For each dependency, first checks if there is available slots for both courses taking in consideration tutor's and supp_tutor's
        availabilities, NoTutorCourseOnDay constraints and possible start times. Then we check if we still have slots for the second one
        starting after the first one and then if the options are True and or above 0 we check successive slots and the day gap.

        Parameter:
            week (Week): the week we want to analyse the data from
            
        Returns:
            JsonResponse: with status 'KO' or 'OK' and a list of messages explaining the problem"""
        dependencies = self.considered_dependecies().filter(Q(course1__week=week) | Q(course1__week=None), Q(course2__week=week) | Q(course2__week=None))
        jsondict = {"status" : _("OK"), "messages" : [], "period": { "week": week.nb, "year": week.year}}  
        for dependency in dependencies:
            ok_so_far = True
            # Setting up empty partitions for both courses
            week_partition_course1 = Partition.get_available_partition_for_course(dependency.course1, week, self.department)
            week_partition_course2 = Partition.get_available_partition_for_course(dependency.course2, week, self.department)
            if week_partition_course1 and week_partition_course2:
                # Retrieving possible start times for both courses
                course1_start_times = CourseStartTimeConstraint.objects.get(course_type = dependency.course1.type).allowed_start_times
                course2_start_times = CourseStartTimeConstraint.objects.get(course_type = dependency.course2.type).allowed_start_times
                # Retrieving only TimeInterval for each course
                course1_slots = week_partition_course1.find_all_available_timeinterval_with_key_starting_at("user_preference", course1_start_times, dependency.course1.type.duration)
                course2_slots = week_partition_course2.find_all_available_timeinterval_with_key_starting_at("user_preference", course2_start_times, dependency.course2.type.duration)
                if course1_slots and course2_slots:
                    while course2_slots[0].end < course1_slots[0].start + timedelta(hours = dependency.course1.type.duration/60+dependency.course2.type.duration/60):
                        course2_slots.pop(0)
                        if not course2_slots:
                            break
                    if course2_slots:
                        if course1_slots[0].start + timedelta(hours = dependency.course1.type.duration/60) > course2_slots[0].start:
                            course2_slots[0].start = course1_slots[0].start + timedelta(hours = dependency.course1.type.duration/60)
                        # Here we check if the first course_slot that we might just shrank is still long enough and if it is the only
                        # one left.
                        if len(course2_slots) <= 1 and course2_slots[0].duration < dependency.course2.type.duration:
                            jsondict["status"] = _("KO")
                            ok_so_far = False
                            jsondict["messages"].append({ "str" : _(f'There is no available slots for the second course after the first one. {dependency}'),
                                                            "course1": dependency.course1.id,
                                                            "course2": dependency.course2.id })
                    else:
                        jsondict["status"] = _("KO")
                        ok_so_far = False
                        jsondict["messages"].append({ "str" : _(f'There is no available slots for the second course after the first one. {dependency}'),
                                                            "course1": dependency.course1.id,
                                                            "course2": dependency.course2.id })
                else:
                    jsondict['status'] = _("KO")
                    ok_so_far = False
                    jsondict["messages"].append({ "str": _(f'There is no available slots for the first or the second course. {dependency}'),
                                                            "course1": dependency.course1.id,
                                                            "course2": dependency.course2.id })

                if ok_so_far:
                    if dependency.successive:
                        if not find_successive_slots(
                            course1_slots,
                            course2_slots,
                            timedelta(hours = dependency.course1.type.duration/60),
                            timedelta(hours = dependency.course2.type.duration/60)):
                            jsondict['status'] = _("KO")
                            ok_so_far = False
                            jsondict["messages"].append({ "str": _(f'There is no available successive slots for those courses. {dependency}'),
                                                            "course1": dependency.course1.id,
                                                            "course2": dependency.course2.id })
                    if dependency.day_gap != 0:
                        if not find_day_gap_slots(course1_slots, course2_slots, dependency.day_gap):
                            jsondict['status'] = _("KO")
                            ok_so_far = False
                            jsondict["messages"].append({ "str": _(f'There is no available slots for the second course after a {dependency.day_gap} day gap. {dependency}'),
                                                            "course1": dependency.course1.id,
                                                            "course2": dependency.course2.id })
            else:
                jsondict['status'] = _("KO")
                ok_so_far = False
                jsondict["messages"].append({ "str": _(f'One of the courses has no eligible tutor to lecture it. {dependency}'),
                                                            "course1": dependency.course1.id,
                                                            "course2": dependency.course2.id })
        return jsondict

    def considered_dependecies(self):
        """Returns the depencies that have to be considered"""
        result=Dependency.objects.filter(course1__type__department=self.department, course2__type__department=self.department)
        if self.train_progs.exists():
            result = result.filter(course1__module__train_prog__in=self.train_progs.all(), course2__module__train_prog__in=self.train_progs.all())
        if self.modules.exists():
            result = result.filter(course1__module__in=self.modules.all(), course2__module__in=self.modules.all())
        if self.weeks.exists():
            result = result.filter(course1__week__in=self.weeks.all(), course2__week__in=self.weeks.all())
        return result

    def one_line_description(self):
        text = f"Prend en compte les précédences enregistrées en base."
        if self.train_progs.exists():
            text += ' des promos ' + ', '.join([train_prog.abbrev for train_prog in self.train_progs.all()])
        if self.modules.exists():
            text += ' pour les modules ' + ', '.join([module.abbrev for module in self.modules.all()])
        return text

    def enrich_model(self, ttmodel, week, ponderation=10):
        if self.train_progs.exists():
            train_progs = set(tp for tp in self.train_progs.all() if tp in ttmodel.train_prog)
        else:
            train_progs = set(ttmodel.train_prog)
        considered_modules = set(ttmodel.wdb.modules)
        if self.modules.exists():
            considered_modules &= set(self.modules.all())

        for p in ttmodel.wdb.dependencies:
            c1 = p.course1
            c2 = p.course2
            if (c1.module not in considered_modules and c2.module not in considered_modules) or \
                    (c1.module.train_prog not in train_progs and c2.module.train_prog not in train_progs):
                continue
            if c1 == c2:
                ttmodel.add_warning(None, "Warning: %s is declared depend on itself" % c1)
                continue
            for sl1 in ttmodel.wdb.compatible_slots[c1]:
                if not self.weight:
                    ttmodel.add_constraint(1000000 * ttmodel.TT[(sl1, c1)] +
                                           ttmodel.sum(ttmodel.TT[(sl2, c2)] for sl2 in ttmodel.wdb.compatible_slots[c2]
                                                       if not sl2.is_after(sl1)
                                                       or (p.ND and (sl2.day == sl1.day))
                                                       or (p.successive and not sl2.is_successor_of(sl1))),
                                           '<=', 1000000, DependencyConstraint(c1, c2, sl1))
                else:
                    for sl2 in ttmodel.wdb.compatible_slots[c2]:
                        if not sl2.is_after(sl1) \
                                or (p.ND and (sl2.day == sl1.day)) \
                                or (p.successive and not sl2.is_successor_of(sl1)):
                            conj_var = ttmodel.add_conjunct(ttmodel.TT[(sl1, c1)],
                                                            ttmodel.TT[(sl2, c2)])
                            ttmodel.add_to_generic_cost(conj_var * self.local_weight() * ponderation)

# Ex TTConstraints that have to be re-written.....


class AvoidBothTimes(TTConstraint):
    """
    Avoid the use of two slots
    Idéalement, on pourrait paramétrer slot1, et slot2 à partir de slot1... Genre slot1
    c'est 8h n'importe quel jour, et slot2 14h le même jour...
    """
    time1 = models.PositiveSmallIntegerField()
    time2 = models.PositiveSmallIntegerField()
    group = models.ForeignKey('base.StructuralGroup', null=True, on_delete=models.CASCADE)
    tutor = models.ForeignKey('people.Tutor',
                              null=True,
                              default=None,
                              on_delete=models.CASCADE)

    @classmethod
    def get_viewmodel_prefetch_attributes(cls):
        attributes = super().get_viewmodel_prefetch_attributes()
        attributes.extend(['group', 'tutor'])
        return attributes

    def enrich_model(self, ttmodel, week, ponderation=1):
        fc = self.get_courses_queryset_by_attributes(ttmodel, week)
        slots1 = set([slot for slot in ttmodel.wdb.courses_slots
                      if slot.start_time <= self.time1 < slot.end_time])
        slots2 = set([slot for slot in ttmodel.wdb.courses_slots
                      if slot.start_time <= self.time2 < slot.end_time])
        for c1 in fc:
            for c2 in fc.exclude(id__lte=c1.id):
                for sl1 in slots1:
                    for sl2 in slots2:
                        if self.weight is not None:
                            conj_var = ttmodel.add_conjunct(
                                ttmodel.TT[(sl1, c1)],
                                ttmodel.TT[(sl2, c2)])
                            ttmodel.add_to_generic_cost(self.local_weight() * ponderation * conj_var, week=week)
                        else:
                            ttmodel.add_constraint(ttmodel.TT[(sl1, c1)]
                                                   + ttmodel.TT[(sl2, c2)],
                                                   '<=',
                                                   1,
                                                   Constraint(constraint_type=ConstraintType.AVOID_BOTH_TIME,
                                                              instructors=self.tutor, groups=self.group))

    def one_line_description(self):
        text = f"Pas à la fois à {french_format(self.time1)} et à {french_format(self.time2)}"
        if self.tutor:
            text += ' pour ' + str(self.tutor)
        if self.group:
            text += ' avec le groupe ' + str(self.group)
        if self.train_progs.exists():
            text += ' des promos ' + ', '.join([train_prog.abbrev for train_prog in self.train_progs.all()])
        else:
            text += " de toutes les promos."
        return text
