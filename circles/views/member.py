# Django
from django.shortcuts import render, redirect
from django.contrib.admin.models import ADDITION, CHANGE
from helpers.functions import log
# Circles
from circles.models import Circle
from circles.forms import CircleForm
from circles.decorators import circle_member

@circle_member
def open(request, serial):
    circle = Circle.objects.get(uuid=serial)
    request.session['circle'] = circle.id
    log(
        request.user.id, circle, ADDITION,
        f"opened the circle ({circle.name})."
    )
    return redirect("circles:page", serial)

@circle_member
def exit(request, serial):
    circle = Circle.objects.get(uuid=serial)
    del request.session['circle']
    log(
        request.user.id, circle, ADDITION,
        f"closed the circle ({circle.name})."
    )
    return redirect("user:navigate")

@circle_member
def page(request, serial):
    circle = Circle.objects.get(uuid=serial)
    log(
        request.user.id, circle, ADDITION,
        f"browsed the circle's page ({circle.name})."
    )
    return render(
        request,
        "circles/index.html",
        {   
            'circle': circle,
            'forms': {
                'circle': CircleForm(instance=circle),
            }
        }
    )