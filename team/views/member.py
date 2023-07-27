# Django
from django.contrib.admin.models import CHANGE, DELETION
from django.shortcuts import redirect, render
from django.contrib import messages

# Models
from team.models import Circle
from ping.models import Room
from user.models import Account

# Functions & Decorators
from helpers.functions import log, get_form_errors
from user.decorators import is_authenticated
from team.decorators import is_logined

# Forms
from blog.forms import SignalForm
from team.forms import (
    CircleForm, CircleLoginForm, AddFounderFriendsForm,
    TransferCircleForm
)


@is_authenticated(True)
@is_logined(False)
def login(request):
    if 'circle' not in request.session:
        if request.method == 'POST':
            form = CircleLoginForm(request.POST)
            if form.is_valid():
                query = Circle.objects.filter(name=form.cleaned_data['name'])
                circle = query.first() if query.exists() else None
                if circle != None and circle.user_role(request.user) != None:
                    if circle.check_password(form.cleaned_data['password']):
                        request.session['circle'] = circle.id
                        return redirect("team:browse")
                    else:
                        messages.error(request, "circle password is wrong")
                else: messages.error(request, "circle credentials error")
            else:
                get_form_errors(request, form)
    return redirect('user:back')

@is_authenticated(True)
@is_logined(True)
def browse(request):
    circle = Circle.objects.get(id=request.session.get('circle'))
    return render(
        request,
        "team/index.html",
        {
            'circle': circle,
            'room': Room.objects.get(serial=circle.serial),
            'forms': {
                'circle': CircleForm(instance=circle),
                'friends': AddFounderFriendsForm(instance=circle),
                'transfer':TransferCircleForm(instance=circle),
                'signal': SignalForm
            },
            'column': {
                'left':"groups",
                'right':"forum",
            }
        }
    )

@is_authenticated(True)
@is_logined(True)
def add_founder_friends(request):
    if request.method == 'POST':
        circle = Circle.objects.get(id=request.session['circle'])
        form = AddFounderFriendsForm(request.POST, instance=circle)
        if form.is_valid():
            selected = [int(x) for x in request.POST.getlist('members')]
            if len(selected) > 0:
                circle.members.add(*selected)
                messages.success(request, f"{len(selected)} friend/s added to your circle.")
            messages.error(request, "You did not select any.")
        messages.error(request, "Something went wrong.")
    return redirect("user:back")

@is_authenticated(True)
@is_logined(True)
def transfer(request):
    circle = Circle.objects.get(id=request.session['circle'])
    if request.method == 'POST':
        form = TransferCircleForm(request.POST, instance=circle)
        if form.is_valid():
            messages.info(request, form.cleaned_data['members'])
    return redirect("user:back")

@is_authenticated(True)
@is_logined(True)
def logout(request):
    del request.session['circle']
    return redirect('user:navigate')

@is_authenticated(True)
@is_logined(True)
def leave(request):
    circle = Circle.objects.get(serial=request.session.get('circle'))
    role   = circle.user_role(request.user)
    if role == "member":
        circle.members.remove(request.user)
        log(request.user.id, circle, CHANGE,
            f"left the circle ({circle.name})."
        )
        circle.save()
    elif role == "founder":
        log(request.user.id, circle, DELETION,
            f"deleted the circle ({circle.name})."
        )
        circle.delete()
    return redirect("team:close")