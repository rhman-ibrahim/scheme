# Django
from django.shortcuts import render, redirect
from django.contrib.admin.models import ADDITION, CHANGE
from django.contrib import messages

# Helpers
from helpers.functions import get_form_errors, log
from helpers.decorators import resource

# User
from user.functions import create_a_guest_user

# Circles
from .decorators import circle, founder, member
from .forms import CircleForm
from .models import Circle


@member
def manage(request):
    circle            = Circle.objects.get(id=request.session.get('circle'))
    if circle.founder == request.user:
        return render(
            request,
            "circles/founder.html",
            {
                'circle': circle,
                'forms': {
                    'circle': CircleForm(instance=circle),
                }
            }
        )
    return render(
            request,
            "circles/member.html",
            {
                'circle': circle,
            }
        )

def create(request):
    if  request.method == "POST":
        form = CircleForm(request.POST)
        if not request.user.is_authenticated:
            create_a_guest_user(request)
        if form.is_valid():
            circle         = form.save(commit=False)
            circle.founder = request.user
            circle         = form.save()
            log(request.user.id, circle, ADDITION,
                f"created the circle ({circle.name})."
            )
            request.session['circle'] = f'{circle.id}'
            messages.success(request, "your circle is created successfully")
        else:
            get_form_errors(request, form)
    return redirect("circles:manage")

def open(request, uuid):
    circle = Circle.objects.get(uuid=uuid)
    request.session['circle'] = circle.id
    return redirect("circles:manage")

@circle
def close(request):
    if request.session['circle']: del request.session['circle']
    return redirect("user:navigate")

@resource("user:navigate")
def ask(request, uuid):
    circle = Circle.objects.get(uuid=uuid)
    if not request.user.is_authenticated:
        create_a_guest_user(request)
    circle.requested.add(request.user)
    circle.save()
    log(request.user.id, circle, ADDITION,
        f"requested to join the circle ({circle.name})."
    )
    return redirect("user:navigate")

@founder
def approve(request, cid, uid):
    circle = Circle.objects.get(id=cid)
    user   = circle.requested.get(id=uid)
    circle.members.add(user)
    circle.requested.remove(user)
    circle.save()
    log(request.user.id, circle, CHANGE,
        f"approved ({user.username}) joining the circle ({circle.name})."
    )
    return redirect("circles:manage")

@founder
def reject(request, cid, uid):
    circle = Circle.objects.get(id=cid)
    user   = circle.requested.get(id=uid)
    circle.requested.remove(user)
    circle.save()
    log(request.user.id, circle, CHANGE,
        f"rejected ({user.username}) joining the circle ({circle.name})."
    )
    return redirect("circles:manage")