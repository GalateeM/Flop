import json
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from base.models import Room
from .models import *
from people.models import User


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


def RoomReservationRefuse(request, uuid, **kwargs):
    db_data = {'dept': request.department.abbrev, 'api': reverse('api:api_root'),
               'user_id': request.user.id, 'accept':False}
    return render(request, 'roomreservation/index.html', {'json_data': db_data})


def RoomReservationRequest(request, **kwargs) :
    bad_response = {'status': 'KO', 'more': ''}
    good_response = {'status': 'OK', 'more': ''}

    print(request.POST)

    responsible_id = request.POST.get('responsible')
    room_id = request.POST.get('room')
    reservation_type_id = request.POST.get('reservation_type')

    # Creation of the roomreservation object
    room_reservation = RoomReservation()

    if request.POST.get('periodicity'):
        # Creation of the periodicity object
        periodicity = request.POST.get('periodicity')
        new_periodicity = ReservationPeriodicity()
        new_periodicity.start = periodicity['start']
        new_periodicity.end = periodicity['end']
        new_periodicity.periodicity_type = periodicity['periodicity_type']
        # save of the periodicity object
        new_periodicity.save()
        room_reservation.periodicity = new_periodicity.id

    # Attributes of the roomreservation object
    responsible = User.objects.all().get(id=responsible_id)
    room_reservation.responsible = responsible
    room = Room.objects.all().get(id=room_id)
    room_reservation.room = room
    reservation_type = RoomReservationType.objects.all().get(id=reservation_type_id)
    room_reservation.reservation_type = reservation_type
    title = request.POST.get('title')
    room_reservation.title = title
    description = request.POST.get('description')
    room_reservation.description = description
    room_reservation.email = request.POST.get('email')
    date = request.POST.get('date')
    room_reservation.date = date
    room_reservation.start_time = request.POST.get('start_time')
    room_reservation.end_time = request.POST.get('end_time')
    is_email_confirmation = request.POST.get('email')
    if is_email_confirmation=="true":
        room_reservation.email=True
    else:
        room_reservation.email=False

    # If the owner is the asker of the reservation is the same person
    if room.owner == None or room.owner == responsible_id:
        room_reservation.is_validated = True
    else:
        room_reservation.is_validated = False
    
    # save of the roomreservation object
    room_reservation.save()

    return JsonResponse(good_response)