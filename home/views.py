from django.shortcuts import render
from user.decorators import authentication
from user.forms import SignUpForm, SignInForm, TokenForm
from circles.forms import CircleForm


@authentication(False)
def index(request):
    return render(
        request,
        "home/index.html",
        {
            'forms': {
                'circle': CircleForm
            }
        }
    )

@authentication(False)
def user(request):
    return render(
        request,
        "home/user.html",
        {
            'forms': {
                'circle': CircleForm,
                'signup': SignUpForm,
                'signin': SignInForm,
                'token': TokenForm
            }
        }
    )

@authentication(False)
def circles(request):
    return render(
        request,
        "home/circles.html",
        {
            'forms': {
                'circle': CircleForm
            }
        }
    )

@authentication(False)
def spaces(request):
    return render(
        request,
        "home/spaces.html",
        {
            'forms': {
                'circle': CircleForm
            }
        }
    )

@authentication(False)
def signals(request):
    return render(
        request,
        "home/signals.html",
        {
            'forms': {
                'circle': CircleForm
            }
        }
    )