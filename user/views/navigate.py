# Response
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db.models import Q

# Decorators
from user.decorators import is_authenticated, is_guest

# Models
from team.models import Circle, CircleRequest

# Forms
from team.forms import CircleForm, CircleLoginForm, CircleRequestForm
from mate.forms import ProfilePictureForm, ProfileInfoForm, AccountUsernameForm
from user.forms import PasswordUpdateForm, AccountDeleteForm


def nav(request):
    if request.user.is_authenticated:
        if request.user.is_guest:
            return redirect("user:guest")
        return redirect("user:settings")
    return redirect("home:index")

@is_authenticated(True)
@is_guest(False)
def settings(request):
    return render(
        request,
        "user/index.html",
        {
            'forms': {
                'delete': AccountDeleteForm,
                'info': ProfileInfoForm(instance=request.user.profile),
                'password': PasswordUpdateForm(False),
                'picture': ProfilePictureForm,
                'mate': AccountUsernameForm,
                'circle_request': CircleRequestForm,
                'login': CircleLoginForm,
                'circle': CircleForm
            },
            'column': {
                'icon': 'settings'
            }
        }
    )

@is_authenticated(True)
@is_guest(True)
def guest(request):
    return render(
            request,
            "user/guest.html",
            {
                'forms': {
                    'mate': AccountUsernameForm,
                    'circle_request': CircleRequestForm,
                    'login': CircleLoginForm,
                    'circle': CircleForm
                },
                'column': {
                    'icon': 'settings'
                }
            }
        )


def back(request):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))