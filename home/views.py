# Django
from django.shortcuts import render
# User
from user.models import Account
from user.forms import (
    SignUpForm, SignInForm, VerifyForm, PassWordResetForm
)
# Circles
from team.models import Circle
from team.forms import CircleForm
# Signal
from blog.models import Signal

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