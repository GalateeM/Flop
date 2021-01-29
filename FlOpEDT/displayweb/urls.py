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

from django.urls import path

import displayweb.views as views

app_name="displayweb"

def generate_room_file(department_abbrev):
    """
    From the data stored in the database, fill the room description file, that
    will be used by the website
    :return:
    """   
    with open(os.path.join(settings.BASE_DIR, 'base',
                           'static', 'base',
                           'rooms.json'), 'w') as fp:
        json.dump(get_rooms(department_abbrev), fp)

def generate_single_room_file(department_abbrev):
    """
    From the data stored in the database, fill the room description file, that
    will be used by the website
    :return:
    """
    with open(os.path.join(settings.BASE_DIR, 'base',
                           'static', 'base',
                           'single_rooms.json'), 'w') as fp:
        json.dump(get_single_rooms(department_abbrev), fp)

urlpatterns = [
    path('fetch_rectangle_colors',
         views.fetch_rectangle_colors,
         name="fetch_colors"),
]