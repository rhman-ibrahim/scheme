# Django
from django.contrib.admin.models import CHANGE, DELETION
from django.shortcuts import redirect, render
from django.contrib import messages
from django.db.models import Q

# Functions & Decorators
from helpers.functions import log, get_form_errors
from user.decorators import is_authenticated
from team.decorators import is_logined

# Forms
from team.forms import CircleForm, CircleLoginForm

# Models
from ping.models import Room
from team.models import Circle


@is_authenticated(True)
@is_logined(False)
def login(request):
    if 'circle' not in request.session:
        if request.method == 'POST':
            form = CircleLoginForm(request.POST)
            if form.is_valid():
                circle = Circle.objects.filter(name=form.cleaned_data['name'])
                if circle.exists() and circle.first().user_role(request.user) != None:
                    if circle.first().check_password(form.cleaned_data['password']):
                        messages.success(request, "welcome")
                        request.session['circle'] = circle.id
                    else: messages.error(request, "circle password is wrong")
                else: messages.error(request, "circle credentials error")
            else:
                get_form_errors(request, form)
    messages.warning(request, "you have to logout from the current circle")
    return redirect('user:back')

@is_authenticated(True)
@is_logined(True)
def browse(request):
    circle = Circle.objects.get(id=request.session.get('circle'))
    return render(
        request,
        "team/index.html",
        {
            'forms': {
                'circle': CircleForm(instance=circle)
            },
            'circle': circle,
            'room': Room.objects.get(serial=circle.serial),
            'column': {
                'icon':"forum",
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