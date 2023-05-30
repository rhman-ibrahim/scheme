# Django
from django.shortcuts import render

# User
from user.forms import SignUpForm, SignInForm, TokenForm
from user.decorators import authentication

# Circles
from circles.forms import CircleForm


context = {
    'signup': SignUpForm,
    'signin': SignInForm,
    'circle': CircleForm
}

@authentication(False)
def index(request):
    return render(
        request,
        "home/_.html",
        {
            'forms':context
        }
    )

@authentication(False)
def user(request):
    return render(
        request,
        "home/user.html",
        {
            'forms':context
        }
    )

@authentication(False)
def circles(request):
    return render(
        request,
        "home/circles.html",
        {
            'forms':context
        }
    )

@authentication(False)
def signals(request):
    return render(
        request,
        "home/signals.html",
        {
            'forms':context
        }
    )

@authentication(False)
def spaces(request):
    return render(
        request,
        "home/spaces.html",
        {
            'forms':context
        }
    )

@authentication(False)
def tasks(request):
    return render(
        request,
        "home/tasks.html",
        {
            'forms':context
        }
    )