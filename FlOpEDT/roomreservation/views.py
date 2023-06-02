import json
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from base.models import Room
from .models import *
from people.models import User

import uuid
from django.core.mail import EmailMessage


@login_required
def RoomReservationsView(request, **kwargs):
    db_data = {'dept': request.department.abbrev, 'api': reverse('api:api_root'),
               'user_id': request.user.id}
    return render(request, 'roomreservation/index.html', {'json_data': db_data})

def RoomReservationAccept(request, uuid, **kwargs):
    db_data = {'dept': request.department.abbrev, 'api': reverse('api:api_root'),
               'user_id': request.user.id, 'accept':True}
    try:
        reservation_request = RoomReservation.objects.all().get(id_mail_validation=uuid)
    except:
        db_data['error'] = True

    print(reservation_request.is_validated)
    if(reservation_request.is_validated==True):
        db_data['first_click']=False
    else:
        db_data['first_click']=True
        reservation_request.is_validated=True
        if len(reservation_request.title.split("]")) > 1:
            reservation_request.title = reservation_request.title.split("]")[1]
        reservation_request.save()
    return render(request, 'roomreservation/index.html', {'json_data': db_data})


def RoomReservationRefuse(request, uuid, **kwargs):
    db_data = {'dept': request.department.abbrev, 'api': reverse('api:api_root'),
               'user_id': request.user.id, 'accept':False}
    return render(request, 'roomreservation/index.html', {'json_data': db_data})
