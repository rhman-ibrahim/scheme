# Django
from django.shortcuts import redirect
from django.contrib.admin.models import ADDITION, CHANGE
from django.contrib import messages
# Helpers
from helpers.functions import get_form_errors, log
# User
from user.functions import create_a_guest_user
# Circles
from circles.forms import CircleForm
from circles.models import Circle
from django.db import IntegrityError


def create(request):
    if  request.method == "POST":
        form = CircleForm(request.POST)
        if not request.user.is_authenticated:
            create_a_guest_user(request)
        try:
            if form.is_valid():
                circle         = form.save(commit=False)
                circle.founder = request.user
                circle         = form.save()
                log(request.user.id, circle, ADDITION,
                    f"created the circle ({circle.name})."
                )
                request.session['circle'] = f'{circle.serial}'
                messages.success(request, "your circle is created successfully")
            else:
                get_form_errors(request, form)
        except IntegrityError:
            messages.warning(request, "you have a circle with this name")
            return redirect("user:navigate")
    return redirect("circle:open", circle.serial)

def link(request, serial):
    circle = Circle.objects.get(serial=serial)
    if request.user.is_authenticated:
        if circle.user_role(request.user):
            messages.info(request, "you are already a membre.")
            return redirect("user:navigate")
    else:
        create_a_guest_user(request)
    circle.requested.add(request.user)
    circle.save()
    messages.success(request, "join request sent successfully.")
    log(
        request.user.id, circle, ADDITION,
        f"requested to join the circle ({circle.name})."
    )
    return redirect("user:navigate")