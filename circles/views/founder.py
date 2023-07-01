# Django
from django.shortcuts import render, redirect
from django.contrib.admin.models import CHANGE
# Spaces
from spaces.models import Room
# User
from user.decorators import is_authenticated
from user.functions import log
# Circles
from circles.models import Circle

    
@is_authenticated(True)
def approve(request, user_id):
    circle = Circle.objects.get(serial=request.session.get('circle'))
    user   = circle.requested.get(id=int(user_id))
    circle.members.add(user)
    circle.requested.remove(user)
    circle.save()
    log(
        request.user.id, circle, CHANGE,
        f"approved ({user.username}) joining the circle ({circle.name})."
    )
    return redirect("circle:browse")    

@is_authenticated(True)
def reject(request, user_id):
    circle = Circle.objects.get(serial=request.session.get('circle'))
    user   = circle.requested.get(id=int(user_id))
    circle.requested.remove(user)
    circle.save()
    log(
        request.user.id, circle, CHANGE,
        f"rejected ({user.username}) joining the circle ({circle.name})."
    )
    return redirect("circle:browse")

@is_authenticated(True)
def remove(request, user_id):
    circle = Circle.objects.get(serial=request.session.get('circle'))
    user = circle.members.get(id=int(user_id))
    circle.members.remove(user)
    circle.save()
    log(
        request.user.id, circle, CHANGE,
        f"removed ({user.username}) from the circle ({circle.name})."
    )
    return redirect("circle:browse")

@is_authenticated(True)
def refresh(request):
    circle = Circle.objects.get(serial=request.session.get('circle'))
    room = Room.objects.get(serial=request.session.get('circle'))
    room.members.set([circle.founder, *circle.members.all()])
    return redirect("circle:browse")