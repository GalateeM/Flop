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

from django.contrib.postgres.fields import ArrayField

from django.db import models

from django.db.models import F

from base.timing import Day

from TTapp.ilp_constraint.constraint_type import ConstraintType
from TTapp.ilp_constraint.constraint import Constraint
from TTapp.slots import Slot, days_filter, slots_filter
from TTapp.TTconstraint import TTConstraint


class LimitCourseTypeTimePerPeriod(TTConstraint):  # , pond):
    """
    Bound the number of courses of type 'type' per day/half day
    """
    course_type = models.ForeignKey('base.CourseType', on_delete=models.CASCADE)
    max_hours = models.PositiveSmallIntegerField()
    modules = models.ManyToManyField('base.Module',
                                     blank=True,
                                     related_name="Course_type_limits")
    tutors = models.ManyToManyField('people.Tutor',
                                    blank=True,
                                    related_name="Course_type_limits")
    FULL_DAY = 'fd'
    HALF_DAY = 'hd'
    PERIOD_CHOICES = ((FULL_DAY, 'Full day'), (HALF_DAY, 'Half day'))
    period = models.CharField(max_length=2, choices=PERIOD_CHOICES)

    def get_courses_queryset(self, ttmodel, train_prog=None, tutor=None, module=None):
        """
        Filter courses depending on constraints parameters
        """
        courses_qs = ttmodel.wdb.courses.filter(type=self.course_type)
        courses_filter = {}

        if tutor is not None:
            courses_filter['tutor'] = tutor

        if module is not None:
            courses_filter['module'] = module

        if train_prog is not None:
            courses_filter['module__train_prog'] = train_prog

        return courses_qs.filter(**courses_filter)

    def register_expression(self, ttmodel, period_by_day, ponderation, train_prog=None, tutor=None, module=None):

        courses = set(self.get_courses_queryset(ttmodel, train_prog, tutor, module))

        for day, period in period_by_day:
            expr = ttmodel.lin_expr()
            if period is None:
                slots = slots_filter(ttmodel.wdb.courses_slots, day=day)
            else:
                slots = slots_filter(ttmodel.wdb.courses_slots, day=day, apm=period)

            for slot in slots:
                for course in courses & ttmodel.wdb.compatible_courses[slot]:
                    expr += ttmodel.TT[(slot, course)] * self.course_type.duration

            if self.weight is not None:
                var = ttmodel.add_floor(
                                'limit course type per period',
                                expr,
                                int(self.max_hours * 60) + 1, 3600*24)
                ttmodel.obj += self.local_weight() * ponderation * var
            else:
                ttmodel.add_constraint(expr, '<=', self.max_hours*60,
                                       Constraint(constraint_type=ConstraintType.MAX_HOURS,
                                                  modules=self.course_type, days=day))

    def enrich_model(self, ttmodel, week, ponderation=1.):

        if self.period == self.FULL_DAY:
            periods = [None]
        else:
            periods = ttmodel.possible_apms

        period_by_day = []
        for day in days_filter(ttmodel.wdb.days, week=week):
            for period in periods:
                period_by_day.append((day, period,))

        try:
            if self.tutors.count():
                for tutor in self.tutors.all():
                    self.register_expression(ttmodel, period_by_day, ponderation, tutor=tutor)
            elif self.modules.count():
                for module in self.modules.all():
                    self.register_expression(ttmodel, period_by_day, ponderation, module=module)
            elif self.train_progs.count():
                for train_prog in self.train_progs.all():
                    self.register_expression(ttmodel, period_by_day, ponderation, train_prog=train_prog)
            else:
                self.register_expression(ttmodel, period_by_day, ponderation)
        except ValueError:
            self.register_expression(ttmodel, period_by_day, ponderation)

    def full_name(self):
        return "Limit Course Type Per Period"

    @classmethod
    def get_viewmodel_prefetch_attributes(cls):
        attributes = super().get_viewmodel_prefetch_attributes()
        attributes.extend(['modules', 'tutors', 'course_type'])
        return attributes

    def get_viewmodel(self):
        view_model = super().get_viewmodel()

        if self.course_type:
            type_value = self.course_type.name
        else:
            type_value = 'All'

        if self.modules:
            module_value = ', '.join([module.abbrev for module in self.modules.all()])
        else:
            module_value = 'All'

        if self.tutors:
            tutor_value = ', '.join([tutor.username for tutor in self.tutors.all()])
        else:
            tutor_value = 'All'

        view_model['details'].update({
            'course_type': type_value,
            'tutor': tutor_value,
            'modules': module_value, })

        return view_model

    def one_line_description(self):
        text = "Pas plus de " + str(self.max_hours) + ' heures de ' + str(self.course_type)
        if self.modules.exists():
            text += " de " + ', '.join([module.abbrev for module in self.modules.all()])
        text += " par "
        if self.period == self.FULL_DAY:
            text += 'jour'
        else:
            text += 'demie-journée'
        if self.tutors.exists():
            text += ' pour ' + ', '.join([tutor.username for tutor in self.tutors.all()])
        if self.train_progs.exists():
            text += ' en ' + ', '.join([train_prog.abbrev for train_prog in self.train_progs.all()])

        return text


class Stabilize(TTConstraint):
    """
    Allow to realy stabilize the courses of a category
    If general is true, none of the other (except week and work_copy) is
    relevant.
    --> In this case, each course c placed:
        - in a unused slot costs 1,
        - in a unused half day (for tutor and/or group) cost ponderation
    If general is False, it Fixes train_prog/tutor/group courses (or tries to if
    self.weight)
    """
    general = models.BooleanField(
        verbose_name='Stabiliser tout?',
        default=False)

    group = models.ForeignKey('base.Group', null=True, default=None, on_delete=models.CASCADE)
    module = models.ForeignKey('base.Module', null=True, default=None, on_delete=models.CASCADE)
    tutor = models.ForeignKey('people.Tutor',
                              null=True,
                              default=None,
                              on_delete=models.CASCADE)
    type = models.ForeignKey('base.CourseType', null=True, default=None, on_delete=models.CASCADE)
    work_copy = models.PositiveSmallIntegerField(default=0)
    fixed_days = ArrayField(models.CharField(max_length=2,
                                             choices=Day.CHOICES), blank=True, null=True)

    @classmethod
    def get_viewmodel_prefetch_attributes(cls):
        attributes = super().get_viewmodel_prefetch_attributes()
        attributes.extend(['group', 'module', 'tutor', 'type'])
        return attributes

    def enrich_model(self, ttmodel, week, ponderation=1):
        sched_courses = ttmodel.wdb.sched_courses.filter(work_copy=self.work_copy, course__week=week)
        if self.fixed_days:
            pass
            # Attention, les fixed_days doivent être des couples jour-semaine!!!!
            # for day in days_filter(self.fixed_days.all(), week=week):
            #     for sc in sched_courses.filter(slot__jour=day):
            #         ttmodel.add_constraint(ttmodel.TT[(sc.slot, sc.course)], '==', 1)
            #     for sc in sched_courses.exclude(slot__day=day):
            #         for sl in ttmodel.wdb.slots.filter(day=day):
            #             ttmodel.add_constraint(ttmodel.TT[(sl, sc.course)], '==', 0)

        if self.general:
            # nb_changements_I=dict(zip(ttmodel.wdb.instructors,[0 for i in ttmodel.wdb.instructors]))
            for sl in slots_filter(ttmodel.wdb.courses_slots, week=week):
                for c in ttmodel.wdb.compatible_courses[sl]:
                    if not sched_courses.filter(start_time__lt=sl.end_time,
                                                start_time__gt=sl.start_time - F('course__type__duration'),
                                                day=sl.day,
                                                course__tutor=c.tutor):
                        ttmodel.obj += ponderation * ttmodel.TT[(sl, c)]
                        # nb_changements_I[c.tutor]+=ttmodel.TT[(sl,c)]
                    if not sched_courses.filter(course__tutor=c.tutor,
                                                day=sl.day):
                        ttmodel.obj += ponderation * ttmodel.TT[(sl, c)]
                        # nb_changements_I[i]+=ttmodel.TT[(sl,c)]
                    for g in c.groups.all():
                        if not sched_courses.filter(course__groups=g,
                                                    day=sl.day):
                            ttmodel.obj += ponderation * ttmodel.TT[(sl, c)]
        else:
            fc = ttmodel.wdb.courses.filter(week=week)
            if self.tutor is not None:
                fc = fc.filter(tutor=self.tutor)
            if self.type is not None:
                fc = fc.filter(type=self.type)
            if self.train_progs.exists():
                fc = fc.filter(groups__train_prog__in=self.train_progs.all())
            if self.group:
                fc = fc.filter(groups=self.group)
            if self.module:
                fc = fc.filter(module=self.module)
            for c in fc:
                sched_c = ttmodel.wdb \
                    .sched_courses \
                    .get(course=c,
                         work_copy=self.work_copy)
                chosen_slot = Slot(start_time=sched_c.start_time, course_type=sched_c.course.type,
                                   day=sched_c.day)
                chosen_roomgroup = sched_c.room
                if self.weight is not None:
                    ttmodel.obj -= self.local_weight() \
                                   * ponderation * ttmodel.TT[(chosen_slot, c)]

                else:
                    for slot in ttmodel.wdb.courses_slots & ttmodel.wdb.compatible_slots[c]:
                        if not slot.is_simultaneous_to(chosen_slot):
                            ttmodel.add_constraint(ttmodel.TT[(slot, c)],
                                                   '==',
                                                   0,
                                                   Constraint(constraint_type=ConstraintType.STABILIZE_ENRICH_MODEL,
                                                              courses=fc, slots=slot))


    def one_line_description(self):
        text = "Minimiser les changements"
        if self.type:
            text += " pour les " + str(self.type)
        if self.module:
            text += " de " + str(self.module)
        if self.tutor:
            text += ' pour ' + str(self.tutor)
        if self.train_progs.count():
            text += ' en ' + ', '.join([train_prog.abbrev for train_prog in self.train_progs.all()])
        if self.group:
            text += ' du groupe ' + str(self.group)
        text += ': copie ' + str(self.work_copy)
        return text
