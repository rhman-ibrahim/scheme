# Django
from django.contrib.admin.models import CHANGE, DELETION
from django.shortcuts import redirect, render
from django.contrib import messages

# Models
from team.models import Circle
from ping.models import Room

# Functions & Decorators
from helpers.functions import log, get_form_errors
from user.decorators import is_authenticated
from team.decorators import is_logined

# Forms
from team.forms import CircleForm, CircleLoginForm


@is_authenticated(True)
@is_logined(False)
def login(request):
    if 'circle' not in request.session:
        if request.method == 'POST':
            form = CircleLoginForm(request.POST)
            if form.is_valid():
                circle = Circle.objects.filter(name=form.cleaned_data['name'])
                circle = circle.first() if circle.exists() else None
                if circle != None and circle.user_role(request.user) != None:
                    if circle.check_password(form.cleaned_data['password']):
                        request.session['circle'] = circle.id
                        return redirect("team:browse")
                    else:
                        messages.info(request, circle.first().password)
                        messages.error(request, "circle password is wrong")
                else: messages.error(request, "circle credentials error")
            else:
                get_form_errors(request, form)
    messages.warning(request, "login view end")
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
                'circle': CircleForm(instance=circle)
            },
            'column': {
                'left':"groups",
                'right':"forum",
            }
        }
    )

@is_authenticated(True)
@is_logined(True)
def logout(request):
    request.session.pop('circle')
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