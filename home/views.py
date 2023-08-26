# Django
from django.views import View
from django.shortcuts import render

# Models
from user.models import Profile
# from blog.models import Post

# Forms
from user.forms import (
    SignUpForm, SignInForm,
)
from note.forms import (
    KeyForm, PassWordResetForm,
)
from team.forms import SpaceForm
from mate.forms import RequestForm

# Decorators
from helpers.decorators import (
    is_authenticated, resource
)

@is_authenticated(False)
@resource
def retrieve_home_index(request):
    return render(
        request,
        "home/index.html",
        {
            'grid': {
                'title': "Express on your behalf or anonymously.",
                'icon': 'menu'
            },
            'widgets': {
                'about': {
                    'me': Profile.objects.get(user__id=1),
                },
            },
            'forms': {
                'user': {
                    'signup': SignUpForm(auto_id="sign_up_%s"),
                    'signin': SignInForm(auto_id="sign_in_%s"),
                },
                'note': {
                    'reset': PassWordResetForm(False, auto_id="password_reset_%s"),
                    'signin': KeyForm(auto_id=f"sign_in_with_token_%s"),
                    'login': KeyForm(auto_id=f"login_secret_%s")
                },
                'team': {
                    'circle': SpaceForm(auto_id="circle_form_%s"),
                    'request': RequestForm(auto_id="circle_request_%s"),
                    'secret': KeyForm(auto_id=f"verify_secret_%s")
                }
            }
        }
    )

def resource_not_found(request):
    return render(
        request,
        "home/404.html",
        {
            'title':'Resource Not Found.'
        }
    )