# Django
from django.contrib.admin.models import ADDITION
from django.shortcuts import redirect
from django.contrib import messages

from django.db.models import Q

# Functions & Decorators
from user.functions import create_a_guest_user, check_guest_activity
from helpers.functions import get_form_errors, log, secret

# Circles
from team.models import Circle
from team.forms import CircleForm


def create(request):
    if request.user.is_authenticated:
        check_guest_activity(request)
    else:
        create_a_guest_user(request)
    if request.method == "POST":
        form = CircleForm(request.POST)
        if form.is_valid():
            if Circle.objects.filter(name=form.cleaned_data['name'], founder=request.user).exists():
                messages.error(request, 'You have a circle with this name.')
                return redirect('user:nav')
            else:
                circle          = form.save(commit=False)
                circle.founder  = request.user
                circle.password = secret(form.cleaned_data['password'])
                circle          = form.save()
                log(
                    request.user.id, circle, ADDITION,
                    f"created the circle ({circle.name})."
                )
                messages.success(request, "your circle is created successfully")
                return redirect("user:nav")
        else:
            get_form_errors(request, form)
    return redirect("user:back")