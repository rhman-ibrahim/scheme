# Django
from django.shortcuts import render
# User
from user.forms import (
    SignUpForm, SignInForm, VerifyForm, PassWordResetForm
)
from user.decorators import is_authenticated
# Circles
from team.forms import CircleForm


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
            }
        }
    )