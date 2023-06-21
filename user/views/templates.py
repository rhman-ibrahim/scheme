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