# Django
from django.http import HttpResponse
from django.contrib.admin.models import CHANGE
from django.shortcuts import render, redirect
# Scheme
from scheme.settings import MEDIA_ROOT
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

@is_authenticated(True)
@is_guest(False)
def token(request):
    with open(f"{MEDIA_ROOT}/user/tokens/{request.user.username}.png", 'rb') as f:
        file = f.read()
    response = HttpResponse(content_type='image/png')
    response.write(file)
    return response