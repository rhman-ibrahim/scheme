# Django
from django.shortcuts import redirect
from django.contrib.admin.models import ADDITION, CHANGE
from django.contrib import messages

# Functions & Decorators
from helpers.functions import get_form_errors, log
from user.functions import create_a_guest_user
from team.decorators import is_logined

# Circles
from team.forms import CircleForm
from team.models import Circle, CircleRequest



@is_logined(False)
def create(request):
    if request.method == "POST":
        form = CircleForm(request.POST)
        if not request.user.is_authenticated: create_a_guest_user(request)
        if form.is_valid():
            if Circle.objects.filter(name=form.cleaned_data['name'], founder=request.user).exists():
                messages.error(request, 'You have a circle with this name.')
                redirect('user:back')
            else:
                circle         = form.save(commit=False)
                circle.set_password(form.cleaned_data['password'])
                circle.founder = request.user
                circle         = form.save()
                log(
                    request.user.id, circle, ADDITION,
                    f"created the circle ({circle.name})."
                )
                messages.success(request, "your circle is created successfully")
        else:
            get_form_errors(request, form)
    return redirect("user:back")

@is_logined(False)
def create_request(request, serial):
    circle = Circle.objects.get(serial=serial)
    if request.user.is_authenticated:
        if circle.user_role(request.user):
            messages.info(request, "you are already a membre.")
            return redirect("user:navigate")
    else:
        create_a_guest_user(request)
    CircleRequest.objects.create(
        circle = circle,
        user   = request.user
    )
    messages.success(
        request,
        "join request sent successfully."
    )
    log(
        request.user.id, circle, ADDITION,
        f"requested to join the circle ({circle.name})."
    )
    return redirect("user:navigate")