# Django
from django.shortcuts import render

# Models
from mate.models import Profile
# from blog.models import Post

# Forms
from user.forms import (
    SignUpForm, SignInForm,
    VerifyForm, PassWordResetForm
)
from team.forms import (
    CircleForm, CircleRequestForm
)

# Decorators
from helpers.decorators import (
    is_authenticated, resource, back
)

@back
def cancel(request):
    request.session.pop('token')

def resource_not_found(request):
    return render(
        request,
        "home/404.html",
        {
            'title':'.sch | Resource Not Found.'
        }
    )
 
@is_authenticated(False)
@resource
def retrieve_home_index(request):
    return render(
        request,
        "home/index.html",
        {
            'forms': {
                'circle_request': CircleRequestForm(auto_id="circle_request_%s"),
                'reset': PassWordResetForm(False, auto_id="password_reset_%s"),
                'circle': CircleForm(auto_id="circle_form_%s"),
                'signup': SignUpForm(auto_id="sign_up_%s"),
                'signin': SignInForm(auto_id="sign_in_%s"),
                'token': {
                    'sign_in': VerifyForm(auto_id=f"sign_in_with_token_%s"),
                    'verify': VerifyForm(auto_id=f"verify_token_%s")
                }
            },
            'about': {
                'me': Profile.objects.get(user__id=1)
            },
            'grid': {
                'title': ".sch | Add friends, create circles, express, discuss & poll.",
                'icons': {
                    'left': 'menu',
                    'right': 'bolt'
                }
            },
        }
    )