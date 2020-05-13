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

from django.db import models

from TTapp.helpers.minhalfdays import MinHalfDaysHelperTutor

from TTapp.ilp_constraints.constraint_type import ConstraintType
from TTapp.ilp_constraints.constraint import Constraint
from TTapp.slots import days_filter, slots_filter
from TTapp.TTconstraint import TTConstraint, max_weight


class MinTutorsHalfDays(TTConstraint):
    """
    All courses will fit in a minimum of half days
    Optional: if 2 courses only, possibility to join it
    """
    tutors = models.ManyToManyField('people.Tutor', blank=True)
    join2courses = models.BooleanField(
        verbose_name='If a tutor has 2 or 4 courses only, join it?',
        default=False)

    def enrich_model(self, ttmodel, week, ponderation=1):

        helper = MinHalfDaysHelperTutor(ttmodel, self, week, ponderation)
        considered_tutors = set(ttmodel.wdb.instructors)
        if self.tutors.exists():
            considered_tutors &= set(self.tutors.all())
        for tutor in considered_tutors:
            helper.enrich_model(tutor=tutor)

    def get_viewmodel(self):
        view_model = super().get_viewmodel()
        details = view_model['details']

        if self.tutors.exists():
            details.update({'tutors': ', '.join([tutor.username for tutor in self.tutors.all()])})

        return view_model

    def one_line_description(self):
        text = "Minimise les demie-journées"

        if self.tutors.exists():
            text += ' de : ' + ', '.join([tutor.username for tutor in self.tutors.all()])
        else:
            text += " de tous les profs"

        if self.train_progs.exists():
            text += ' en ' + ', '.join([train_prog.abbrev for train_prog in self.train_progs.all()])

        return text


class MinNonPreferedTutorsSlot(TTConstraint):
    """
    Minimize the use of unprefered Slots for tutors
    """
    tutors = models.ManyToManyField('people.Tutor',
                                    related_name='min_non_prefered_tutors_slots_constraints')

    @classmethod
    def get_viewmodel_prefetch_attributes(cls):
        attributes = super().get_viewmodel_prefetch_attributes()
        attributes.extend(['tutors'])
        return attributes

    def enrich_model(self, ttmodel, week, ponderation=None):
        if ponderation is None:
            ponderation = ttmodel.min_ups_i
        if self.tutors.exists():
            tutors = set(t for t in ttmodel.wdb.instructors if t in self.tutors.all())
        else:
            tutors = set(ttmodel.wdb.instructors)
        for sl in ttmodel.wdb.availability_slots:
            for tutor in tutors:
                filtered_courses = set(c for c in ttmodel.wdb.possible_courses[tutor] if c.week == week)
                for c in filtered_courses:
                    slot_vars_sum = ttmodel.sum(ttmodel.TTinstructors[(sl2, c, tutor)]
                                                for sl2 in slots_filter(ttmodel.wdb.compatible_slots[c],
                                                                        simultaneous_to=sl))
                    cost = (float(self.weight) / max_weight) \
                        * ponderation * slot_vars_sum \
                        * ttmodel.unp_slot_cost[tutor][sl]
                    ttmodel.add_to_inst_cost(tutor, cost, week=week)

    def one_line_description(self):
        text = "Respecte les préférences"
        if self.tutors.exists():
            text += ' de ' + ', '.join([tutor.username for tutor in self.tutors.all()])
        else:
            text += ' de tous les profs.'
        return text


class MinimizeBusyDays(TTConstraint):
    """
    This class is a template for writing your own custom contraint.

    The module can contains several custom constraints.
    """
    tutors = models.ManyToManyField('people.Tutor', blank=True)

    def enrich_model(self, ttmodel, week, ponderation=None):
        """
        Minimize the number of busy days for tutor with cost
        (if it does not overcome the bound expressed in pref_hours_per_day)
        """
        if ponderation is None:
            ponderation = ttmodel.min_bd_i

        for tutor in self.tutors.all():
            slot_by_day_cost = 0
            # need to be sorted
            courses_hours = sum(c.type.duration
                                for c in (ttmodel.wdb.courses_for_tutor[tutor]
                                          | ttmodel.wdb.courses_for_supp_tutor[tutor])
                                & ttmodel.wdb.courses_by_week[week]) / 60
            nb_days = 5
            frontier_pref_busy_days = [tutor.pref_hours_per_day * d for d in range(nb_days - 1, 0, -1)]

            for fr in frontier_pref_busy_days:
                if courses_hours <= fr:
                    slot_by_day_cost *= 2
                    slot_by_day_cost += ttmodel.IBD_GTE[week][nb_days][tutor]
                    nb_days -= 1
                else:
                    break
            ttmodel.add_to_inst_cost(tutor, ponderation * slot_by_day_cost, week=week)

    def get_viewmodel(self):
        view_model = super().get_viewmodel()
        details = view_model['details']

        if self.tutors.exists():
            details.update({'tutors': ', '.join([tutor.username for tutor in self.tutors.all()])})

        return view_model

    def one_line_description(self):
        """
        You can give a contextual explanation about what this constraint doesnt
        """
        return "MinimizeBusyDays online description"

    class Meta:
        verbose_name_plural = "Minimize busy days"


class RespectBoundPerDay(TTConstraint):
    """
    Respect the max_hours_per_day declared
    """
    tutors = models.ManyToManyField('people.Tutor', blank=True)

    def enrich_model(self, ttmodel, week, ponderation=1):
        """
        Minimize the number of busy days for tutor with cost
        (if it does not overcome the bound expressed in pref_hours_per_day)
        """
        for tutor in self.tutors.all():
            for d in days_filter(ttmodel.wdb.days, week=week):
                ttmodel.add_constraint(ttmodel.sum(ttmodel.IBS[tutor, sl] * sl.duration / 60
                                                   for sl in slots_filter(ttmodel.wdb.availability_slots, day=d)),
                                       '<=',
                                       tutor.max_hours_per_day,
                                       Constraint(constraint_type=ConstraintType.BOUND_HOURS_PER_DAY,
                                                  instructors=tutor,
                                                  days=d))

    def get_viewmodel(self):
        view_model = super().get_viewmodel()
        details = view_model['details']

        if self.tutors.exists():
            details.update({'tutors': ', '.join([tutor.username for tutor in self.tutors.all()])})

        return view_model

    def one_line_description(self):
        """
        You can give a contextual explanation about what this constraint doesnt
        """
        return "RespectBoundPerDay online description"

    class Meta:
        verbose_name_plural = "Respecter les limites horaires"


class LowerBoundBusyDays(TTConstraint):
    """
    Impose a minimum number of days if the number of hours is higher than a lower bound
    """
    tutor = models.ForeignKey('people.Tutor', on_delete=models.CASCADE)
    min_days_nb = models.PositiveSmallIntegerField()
    lower_bound_hours = models.PositiveSmallIntegerField()

    def enrich_model(self, ttmodel, week, ponderation=1):
        relevant_courses = self.get_courses_queryset_by_attributes(ttmodel, week)

        if sum(c.type.duration for c in relevant_courses) > self.lower_bound_hours:
            ttmodel.add_constraint(ttmodel.IBD_GTE[self.min_days_nb][self.tutor], '==', 1,
                                   Constraint(constraint_type='LowerBoundBusyDays', instructors=self.tutor))

    def one_line_description(self):
        return f"Si plus de {self.lower_bound_hours} heures pour {self.tutor}  alors au moins {self.min_days_nb} jours"

    def get_viewmodel(self):
        view_model = super().get_viewmodel()

        view_model['details'].update({
            'tutor': self.tutor.username,
        })

        return view_model
