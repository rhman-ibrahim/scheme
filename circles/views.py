from itertools import chain
from operator import attrgetter



from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib import messages

from user.decorators import authenticated
from .models import followRequest, joinRequest, Connection, Circle
from user.models import Account


@authenticated(True)
def connect(request):
    receivers   = [call.receiver for call in followRequest.objects.filter(sender=request.user)]
    accounts    = list(set(receivers).symmetric_difference(set(Account.objects.all().exclude(username=request.user.username))))
    connections = sorted(chain(accounts, Circle.objects.all()), key=attrgetter('created'))
    return render(
        request,
        "circles/connect.html",
        {
            'connections': {
                'list': connections,
                'requests': followRequest.objects.filter(receiver=request.user, status=0)
            }
        }
    )

@authenticated(True)
def create_connection(request, username):
    try:
        followRequest.objects.create(sender=request.user, receiver=Account.objects.get(username=username))
        messages.success(request, "connection request was created and sent succesfully.")
    except IntegrityError:
        messages.success(request, "request has been sent succesfully.")
    return redirect("circles:connect")

@authenticated(True)
def accept_connection(request, id):
    followRequest.objects.filter(id=id).update(result=1, status=1)
    follow_request = followRequest.objects.get(id=id)
    connection     = Connection.objects.get_or_create(followee=request.user)
    connection[0].followers.add(follow_request.sender)
    messages.info(request, "connection was opened successfully")
    return redirect("circles:connect")

@authenticated(True)
def reject_connection(request, id):
    followRequest.objects.filter(id=id).update(result=2, status=2)
    messages.info(request, "connection was closed successfully")
    return redirect("circles:connect")

@authenticated(True)
def home(request):
    return render(request, "circles/home.html")
    
@authenticated(True)
def manage(request):
    return render(request, "circles/manage.html")