import json
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse

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
        if(reservation_request.is_validated==True):
            db_data['first_click']=False
        else:
            db_data['first_click']=True
            reservation_request.is_validated=True
            if len(reservation_request.title.split("]")) > 1:
                reservation_request.title = reservation_request.title.split("]")[1]
            reservation_request.save()
            send_mail(True, reservation_request)
        return render(request, 'roomreservation/index.html', {'json_data': db_data})
    except:
        db_data['error'] = True
        return render(request, 'roomreservation/index.html', {'json_data': db_data})


def RoomReservationRefuse(request, uuid, **kwargs):
    db_data = {'dept': request.department.abbrev, 'api': reverse('api:api_root'),
               'user_id': request.user.id, 'accept':False}
    try:
        #verification de si la reservation existe
        reservation_request = RoomReservation.objects.all().get(id_mail_validation=uuid)
    except:
        db_data['error'] = True
    return render(request, 'roomreservation/index.html', {'json_data': db_data})


def RoomReservationRefuseConfirmed(request, uuid, **kwargs):
    bad_response = {'status': 'KO', 'more': ''}
    good_response = {'status': 'OK', 'more': ''}
    try:
        reservation_request = RoomReservation.objects.all().get(id_mail_validation=uuid)
        reservation_request.delete()
        send_mail(False, reservation_request)
        return JsonResponse(good_response)
    except:
        return JsonResponse(bad_response)

def send_mail(isaccept, reservation):
        msg = f'<p>Bonjour,<br> Votre réservation : <br>'
        msg += 'Salle : '+ reservation.room.name + "<br>"
        msg += 'Horaire : '+ reservation.date.strftime("%d/%m/%Y")
        msg += ' de ' + reservation.start_time.strftime("%H:%M") + " à " + reservation.end_time.strftime("%H:%M") + "<br>"
        
        obj = "[flop!EDT]"
        if isaccept:
            msg += "a été acceptée."
            obj += " Réservation acceptée"
        else:
            msg += "a été refusée."
            obj += " Réservation refusée"

        
        email = EmailMessage(
            obj,
            msg,
            to=(reservation.responsible.email,)
        )
        email.content_subtype = "html"
        email.send()