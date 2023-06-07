# Django
from django.contrib.admin.models import CHANGE
from django.shortcuts import render, redirect
# Circles
from circles.forms import CircleForm
# User
from user.models import Token
from user.forms import  (
    ProfilePictureForm, PasswordUpdateForm,
    ProfileInfoForm, PassWordResetForm
)
from user.decorators import is_authenticated, is_guest
from user.functions import create_a_guest_user


@is_authenticated(True)
@is_guest(False)
def settings(request):
    return render(
        request,
        "user/settings.html",
        {
            'forms': {
                'info': ProfileInfoForm(instance=request.user.profile),
                'password': PasswordUpdateForm(False),
                'picture': ProfilePictureForm,
                'circle': CircleForm
            }
        }
    )

@is_authenticated(False)
def identified(request):
    token = Token.objects.get(value=request.session['token'])
    if 'token' in request.session:
        return render(
            request,
            "user/identified.html",
            {
                'user': token.user,
                'forms': {
                    'reset': PassWordResetForm(token.user),
                }
            }
        )
    return redirect('home:user')

def guest(request):
    if not request.user.is_authenticated:
        create_a_guest_user(request)
    elif not request.user.is_guest:
        return redirect("user:settings")
    return render(
        request,
        "user/guest.html",
        {
            'forms': {
                'circle': CircleForm
            }
        }
    )