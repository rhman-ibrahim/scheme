# Django
from django.contrib.admin.models import ADDITION, DELETION
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages
from django.http import Http404
from django.db.models import Q

# Functions & Decorators
from user.functions import create_a_guest_user, check_guest_activity
from helpers.functions import get_form_errors, log, secret
from user.decorators import is_authenticated
from team.decorators import is_logined

# Circles
from team.models import Circle, CircleRequest
from team.forms import CircleForm, CircleRequestForm


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


def create_circle_request(request):
    if request.user.is_authenticated:
        check_guest_activity(request)
    else:
        create_a_guest_user(request)
    if request.method == 'POST':
        try:
            form  = CircleRequestForm(request.POST)
            if form.is_valid():
                # 1: check
                circle = get_object_or_404(Circle, serial=form.cleaned_data['serial'])
                query  = CircleRequest.objects.filter(circle=circle, user=request.user)
                # 2: if the request is there and not rejected (status != 0)
                if query.exists() and query.first().status != 0:
                    if query.first().status == 2:
                        messages.info(request, f"Your request to join {query.first().circle.name} is pending")
                    elif query.first().status == 1:
                        messages.info(request, f"You are already connected to {query.first().circle.name}")
                    return redirect("user:nav")
                else:
                    # 3: if request is not there or it is there and rejected
                    CircleRequest.objects.create(
                        circle=circle,
                        user=request.user
                    )
                    messages.success(
                        request,
                        "join request created successfully."
                        )
                    log(
                        request.user.id, circle, ADDITION,
                        f"requested to join the circle ({circle.name})."
                    )
                    return redirect("user:nav")
            else: get_form_errors(request, form)
        except Http404:messages.error(request, "circle does not exists")
    return redirect("user:back")


@is_authenticated(True)
def delete_circle_request(request, req):
    f_req = CircleRequest.objects.get(id=req)
    f_req.delete()
    messages.success(
        request,
        f"You have cancelled the circle request to {f_req.circle.name}"
    )
    log(request.user.id, f_req, DELETION,
        f"deleted the friend request sent to {f_req.circle.name}"
    )
    return redirect("user:back")