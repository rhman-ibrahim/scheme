# Django
from django.contrib.admin.models import CHANGE, DELETION
from django.shortcuts import redirect, render
from django.contrib import messages

# Models
from team.models import Circle
from ping.models import Room
from blog.models import Signal

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
def settings(request):
    circle = Circle.objects.get(id=request.session.get('circle'))
    return render(
        request,
        "team/settings.html",
        {
            'circle': circle,
            'forms': {
                'circle': CircleForm(instance=circle),
                'friends': AddFounderFriendsForm(instance=circle),
                'transfer':TransferCircleForm(instance=circle),
            },
            'column': {
                'icon':"groups"
            }
        }    
    )

@is_authenticated(True)
@is_logined(True)
def browse(request):
    circle = Circle.objects.get(id=request.session.get('circle'))
    request.session['parent_signal_id'] = None
    return render(
        request,
        "team/index.html",
        {
            'circle': circle,
            'room': Room.objects.get(serial=circle.serial),
            'signals': Signal.objects.filter(circle=circle, level=0).order_by('-created'),
            'forms': {
                'signal': SignalForm
            },
            'column': {
                'left':"format_quote",
                'right':"forum",
            }
        }    
    )

@is_authenticated(True)
@is_logined(True)
def logout(request):
    del request.session['circle']
    return redirect('user:nav')

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