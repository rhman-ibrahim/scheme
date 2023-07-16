# Django
from django.shortcuts import render
from django.contrib import messages
# User
from user.forms import SignUpForm, SignInForm, VerifyForm, PassWordResetForm
from user.decorators import is_authenticated
from user.models import Account
# Circles
from team.forms import CircleForm
from team.models import Circle
# Signal
from blog.models import Signal


@is_authenticated(False)
def index(request):
    return render(
        request,
        "home/index.html",
        {
            'forms': {
                'signup': SignUpForm,
                'signin': SignInForm,
                'circle': CircleForm,
                'verify': VerifyForm,
                'reset': PassWordResetForm(False)
            },
            'stats': {
                'interactions': Signal.objects.count(),
                'circles': Circle.objects.count(),
                'users': Account.objects.count(),
            }
        }
    )