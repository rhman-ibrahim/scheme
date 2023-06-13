# Django
from django.shortcuts import render, redirect
# User
from user.forms import (
    SignUpForm, SignInForm, VerifyForm
)
from user.decorators import is_authenticated
# Circles
from circles.forms import CircleForm


context = {
    'signup': SignUpForm,
    'signin': SignInForm,
    'circle': CircleForm,
    'verify': VerifyForm
}

@is_authenticated(False)
def index(request):
    return render(
        request,
        "home/index.html",
        {
            'forms':context
        }
    )

@is_authenticated(False)
def user(request):
    return render(
        request,
        "home/user.html",
        {
            'forms':context
        }
    )

@is_authenticated(False)
def circles(request):
    return render(
        request,
        "home/circles.html",
        {
            'forms':context
        }
    )

def signals(request):
    if request.user.is_authenticated:
        return redirect("signals:list")
    
    return render(
        request,
        "home/signals.html",
        {
            'forms':context
        }
    )

@is_authenticated(False)
def spaces(request):
    return render(
        request,
        "home/spaces.html",
        {
            'forms':context
        }
    )

@is_authenticated(False)
def tasks(request):
    return render(
        request,
        "home/tasks.html",
        {
            'forms':context
        }
    )