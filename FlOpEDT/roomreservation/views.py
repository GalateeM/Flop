from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
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

