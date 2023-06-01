import json
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from FlOpEDT.base.models import RoomAttribute
from .models import RoomReservation


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
    responsible = json.loads(request.POST.get('responsible'))
    room_attributes = RoomAttribute.objects.get(responsible)

    # Creation of the RoomReservation object
    room_reservation = RoomReservation()
    room_reservation.responsible = responsible
    room_reservation.room = json.loads(request.POST.get('room'))
    room_reservation.reservation_type = json.loads(request.POST.get('reservation_type'))
    room_reservation.title = json.loads(request.POST.get('title'))
    room_reservation.description = json.loads(request.POST.get('description'))
    room_reservation.email = json.loads(request.POST.get('email'))
    room_reservation.date = json.loads(request.POST.get('date'))
    room_reservation.start_time = json.loads(request.POST.get('start_time'))
    room_reservation.end_time = json.loads(request.POST.get('end_time'))
    room_reservation.periodicity = json.loads(request.POST.get('periodicity'))
    room_reservation.is_validated = False

    # If the owner is the asker of the reservation is the same person
    if room_attributes['owner'] == responsible :
        room_reservation.is_validated = True
    
    room_reservation.save()