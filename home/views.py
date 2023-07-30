# Django
from django.shortcuts import render
# User
from user.forms import SignUpForm, SignInForm, VerifyForm, PassWordResetForm
from user.decorators import is_authenticated
from user.models import Account
from mate.models import Profile
# Circles
from team.forms import CircleForm, CircleRequestForm
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
                'circle_request': CircleRequestForm,
                'reset': PassWordResetForm(False),
                'signup': SignUpForm,
                'signin': SignInForm,
                'circle': CircleForm,
                'verify': VerifyForm
            },
            'stats': {
                'interactions': Signal.objects.count(),
                'circles': Circle.objects.count(),
                'users': Account.objects.count(),
            },
            'column': {
                'icon': 'person'
            },
            'about': {
                'me': Profile.objects.get(user__id=1)
            }
        }
    )