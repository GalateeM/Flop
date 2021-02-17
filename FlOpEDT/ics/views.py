from django.shortcuts import render

from people.models import Tutor
from base.models import Group, Room
import base.queries as queries

def index(request, **kwargs):
    tutor_list = Tutor.objects.filter(is_active=True, is_tutor=True)\
                              .prefetch_related('departments')\
                              .order_by('username')
    group_list = Group.objects.filter(
        basic=True,
        train_prog__department=request.department
    )\
                              .select_related('train_prog__department')\
                              .order_by('train_prog__abbrev', 'name')
    room_list = [{'name':n.name, 'id':n.id}
                  for n in queries.get_rooms(None, basic=True).order_by('name')]
    # We consider suffix length to avoid ics link representation
    suffix_length = len(request.department.abbrev) + 6
    context = {'tutors': tutor_list,
               'groups': group_list,
               'rooms': room_list,
               'requi': request.build_absolute_uri()[:-suffix_length]}
    return render(request, 'ics/index.html', context=context)
