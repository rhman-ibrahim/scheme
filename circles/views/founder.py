# Django
from django.shortcuts import render, redirect
from django.contrib.admin.models import ADDITION, CHANGE
# Circles
from circles.models import Circle
from circles.decorators import circle_founder
# User
from user.decorators import is_authenticated
from user.functions import log

    
@is_authenticated(True)
@circle_founder
def approve(request, serial, user_id):
    circle = Circle.objects.get(uuid=str(serial))
    user   = circle.requested.get(id=int(user_id))
    circle.members.add(user)
    circle.requested.remove(user)
    circle.save()
    log(
        request.user.id, circle, CHANGE,
        f"approved ({user.username}) joining the circle ({circle.name})."
    )
    return redirect("circles:page", serial)    

@is_authenticated(True)
@circle_founder
def remove(request, serial, user_id):
    circle = Circle.objects.get(uuid=str(serial))
    user = circle.members.get(id=int(user_id))
    circle.members.remove(user)
    circle.save()
    log(
        request.user.id, circle, CHANGE,
        f"removed ({user.username}) from the circle ({circle.name})."
    )
    return redirect("circles:page", serial)

@is_authenticated(True)
@circle_founder
def reject(request, serial, user_id):
    circle = Circle.objects.get(uuid=str(serial))
    user   = circle.requested.get(id=int(user_id))
    circle.requested.remove(user)
    circle.save()
    log(
        request.user.id, circle, CHANGE,
        f"rejected ({user.username}) joining the circle ({circle.name})."
    )
    return redirect("circles:page", serial)