# Django
from django.shortcuts import render

# Models
from user.models import Profile
# from blog.models import Post

# Forms
from user.forms import (
    TokenForm, PassWordResetForm,
    SignUpForm, SignInForm,
)
from team.forms import CircleForm
from mate.forms import CircleRequestForm

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
            'title':'Resource Not Found.'
        }
    )
 
@is_authenticated(False)
@resource
def retrieve_home_index(request):
    return render(
        request,
        "home/index.html",
        {
            'grid': {
                'title': "Add friends, create circles, express, discuss & poll.",
                'icons': {
                    'left': 'menu',
                    'right': 'bolt'
                }
            },
            'widgets': {
                'about': {
                    'me': Profile.objects.get(user__id=1),
                },
            },
            'forms': {
                'user': {
                    'reset': PassWordResetForm(False, auto_id="password_reset_%s"),
                    'signup': SignUpForm(auto_id="sign_up_%s"),
                    'signin': SignInForm(auto_id="sign_in_%s"),
                    'token': {
                        'signin': TokenForm(auto_id=f"sign_in_with_token_%s"),
                        'verify': TokenForm(auto_id=f"verify_token_%s")
                    }
                },
                'team': {
                    'circle': CircleForm(auto_id="circle_form_%s"),
                    'request': CircleRequestForm(auto_id="circle_request_%s"),
                }
            }
        }
    )