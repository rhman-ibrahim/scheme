# Django
from django.shortcuts import render

# Models
from user.models import Account
from mate.models import Profile
from team.models import Circle
from blog.models import Signal

# Forms
from user.forms import (
    SignUpForm, SignInForm,
    VerifyForm, PassWordResetForm
)
from team.forms import (
    CircleForm, CircleRequestForm
)

# Decorators
from user.decorators import is_authenticated


@is_authenticated(False)
def render_home_index(request):
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