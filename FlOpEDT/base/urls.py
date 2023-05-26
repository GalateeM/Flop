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

from django.urls import re_path, include
from django.urls import path, re_path
from . import views
from . import statistics
from django.views.generic import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

app_name="base"

urlpatterns = [
    # favicon
    # ----------------------------
    path(views.fav_regexp,
        views.favicon,
        name="favicon"),

    # directly reachable by users
    # ----------------------------
    re_path(r'room-preference/(?P<tutor>\w{2,8})?', views.room_preference, name='room-pref'),
    re_path(r'visio-preference/(?P<tutor>\w{1,8})?(/?P<id>\d{1,8})?',
            views.visio_preference,
            name='visio-pref'),

    re_path(r'^preferences$', views.preferences, name="preferences"),
    re_path(r'^semaine-type$', views.stype, name="stype"),
    re_path(r'^aide$', views.aide, name="aide"),
    re_path(r'^decale$', views.decale, name="decale"),    
    re_path(r'^contact/(?P<tutor>\w{2,8})?$', views.contact, name="contact"),
    re_path(r'^module_description(/(?P<module>\w{1,8}))?$', views.module_description, name="module_description"),
    re_path(r'^((?P<year>\d{4}))?(/(?P<week>\d{1,2}))?$', views.edt, name="edt"),
    re_path(r'^tv(/(?P<year>\d+))?(/(?P<week>\d+))?$', views.edt_light, name="edt_light"),
    re_path(r'^modules$', views.all_modules_with_desc, name="modules"),
    #Send Email to teacher when student want modify schedule
    re_path(r'^email-modif$', views.send_email_proposal, name='email-proposal'),
    path('email_test', views.send_email_test, name='send_email_test'),

    # exchanges with the db via django
    # ---------------------------------

    # from db to screen
    path('fetch_user_default_week/<str:username>', views.fetch_user_default_week, name="fetch_user_dweek"),
    path('fetch_course_default_week/<str:train_prog>/<str:course_type>', views.fetch_course_default_week, name="fetch_course_dweek"),
    path('fetch_room_default_week/<str:room>', views.fetch_room_default_week, name="fetch_room_dweek"),
    re_path(r'^fetch_decale$', views.fetch_decale, name="fetch_decale"),
    re_path(r'^fetch_bknews/(?P<year>\d+)/(?P<week>\d+)$', views.fetch_bknews, name="fetch_bknews"),
    re_path(r'^fetch_groups$', views.fetch_groups, name="fetch_groups"),    
    re_path(r'^fetch_rooms$', views.fetch_rooms, name="fetch_rooms"),    
    re_path(r'^fetch_flat_rooms$', views.fetch_flat_rooms, name="fetch_flat_rooms"),    
    re_path(r'^fetch_constraints$', views.fetch_constraints, name="fetch_constraints"),
    path('fetch_course_types', views.fetch_course_types, name="fetch_course_types"),
    path('fetch_training_programmes', views.fetch_training_programmes, name="fetch_training_programmes"),
    re_path(r'^fetch_unavailable_rooms/(?P<year>\d+)/(?P<week>\d+)$', views.fetch_unavailable_rooms, name="fetch_unavailable_rooms"),
    re_path(r'^fetch_all_tutors/$', views.fetch_all_tutors, name="fetch_all_tutors"),
    re_path(r'^fetch_all_versions/$', views.fetch_all_versions, name="fetch_all_versions"),
    path('fetch_departments', views.fetch_departments, name="fetch_departments"),
    path('fetch_tutor_courses/<int:year>/<int:week>/<str:tutor>', views.fetch_tutor_courses, name="fetch_tutor_courses"),
    path('fetch_extra_sched/<int:year>/<int:week>', views.fetch_extra_sched, name="fetch_extra_sched"),
    path('fetch_shared_rooms/<int:year>/<int:week>', views.fetch_shared_rooms, name="fetch_shared_rooms"),
    path('fetch_perfect_day/<str:username>', views.fetch_perfect_day, name="fetch_perfect_day"),
    path('fetch_user_notifications_pref/<str:username>', views.fetch_user_notifications_pref, name="fetch_user_notifications_pref"),
    re_path(r'^fetch_module/(?P<year>\d+)/(?P<week>\d+)$', views.fetch_module, name="fetch_module"),
    re_path(r'^fetch_tutors/(?P<year>\d+)/(?P<week>\d+)$', views.fetch_tutor, name="fetch_tutor"),
    re_path(r'^fetch_all_modules_with_desc$', views.fetch_all_modules_with_desc, name="fetch_all_modules_with_desc"),
    re_path(r'^fetch_all_dispos$', views.fetch_all_dispos, name="fetch_all_dispos"),
    path('fetch_group_preferred_links',
         views.fetch_group_preferred_links,
         name='fetch_group_preferred_links'),

    # statistics
    # ---------------------------------
    path('statistics/', include([
        path('', statistics.index, name="statistics"),
        path('rooms/', statistics.fetch_room_activity, name="room_activity"),
        path('tutors/', statistics.fetch_tutor_hours, name="tutor_hours"),
    ])),

    # from screen to db
    path('change_edt', views.edt_changes, name="edt_changes"),
    path('change_user_pref/<int:year>/<int:week>/<str:username>',
         views.user_preferences_changes,
         name="user_pref_changes"),
    path('change_course_pref/<int:year>/<int:week>/<str:train_prog>/<str:course_type>', views.course_preferences_changes, name="course_pref_changes"),
    path('change_room_pref/<int:year>/<int:week>/<str:room>',
         views.room_preferences_changes,
         name="room_pref_changes"),
    path('change_decale', views.decale_changes, name="decale_changes"),
    path('change_perfect_day/<str:username>',
         views.user_perfect_day_changes,
         name="user_perfect_day_changes"),
    path('change_user_notifications_pref/<str:username>',
         views.user_notifications_pref_changes,
         name="user_notifications_pref_changes"),
    path('change_user_themes_pref/<str:username>',
         views.user_themes_pref_changes,
         name="user_themes_pref_changes"),
    path(r'change_room_pref_per_tutor/<str:tutor>',
         views.room_preferences_changes_per_tutor,
         name='room_pref_changes_per_tutor'),

    # predefined
    # ------------
]

# https://pypi.python.org/pypi/django-live-log
# https://github.com/abdullatheef/django_live_log
