import json
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from base.models import Room
from .models import *


@login_required
def RoomReservationsView(request, **kwargs):
    db_data = {'dept': request.department.abbrev, 'api': reverse('api:api_root'),
               'user_id': request.user.id}
    return render(request, 'roomreservation/index.html', {'json_data': db_data})

def RoomReservationAccept(request, uuid, **kwargs):
    db_data = {'dept': request.department.abbrev, 'api': reverse('api:api_root'),
               'user_id': request.user.id, 'accept':True}
    reservation_request = RoomReservation.objects.all().get(id_mail_validation=uuid)
    print(reservation_request.is_validated)
    if(reservation_request.is_validated==True):
        db_data['first_click']=False
    else:
        db_data['first_click']=True
        reservation_request.is_validated=True
        reservation_request.save()
    return render(request, 'roomreservation/index.html', {'json_data': db_data})

def RoomReservationRequest(request, **kwargs) :
    bad_response = {'status': 'KO', 'more': ''}
    good_response = {'status': 'OK', 'more': ''}

    responsible = json.loads(request.POST.get('responsible'))
    room = json.loads(request.POST.get('room'))
    reservation_type = json.loads(request.POST.get('reservation_type'))

    # Creation of the periodicity object
    periodicity = json.loads(request.POST.get('periodicity'))
    new_periodicity = ReservationPeriodicity()
    new_periodicity.start = periodicity['start']
    new_periodicity.end = periodicity['end']
    new_periodicity.periodicity_type = periodicity['periodicity_type']
    # save of the periodicity object
    new_periodicity.save()

    # Creation of the roomreservation object
    room_reservation = RoomReservation()
    room_reservation.responsible = responsible['id']
    room_reservation.room = room['id']
    room_reservation.reservation_type = reservation_type['id']
    room_reservation.title = json.loads(request.POST.get('title'))
    room_reservation.description = json.loads(request.POST.get('description'))
    room_reservation.email = json.loads(request.POST.get('email'))
    room_reservation.date = json.loads(request.POST.get('date'))
    room_reservation.start_time = json.loads(request.POST.get('start_time'))
    room_reservation.end_time = json.loads(request.POST.get('end_time'))
    room_reservation.periodicity = new_periodicity.id
    room_reservation.is_validated = False

    # If the owner is the asker of the reservation is the same person
    if room['owner'] == responsible['id'] :
        room_reservation.is_validated = True
    
    # save of the roomreservation object
    room_reservation.save()

    return JsonResponse(good_response)