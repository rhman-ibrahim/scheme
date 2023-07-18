# Response
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
# Decorators
from user.decorators import is_authenticated, is_guest
# Forms
from mate.forms import ProfilePictureForm, ProfileInfoForm
from mate.forms import AccountUsernameForm
from user.forms import  PasswordUpdateForm
from team.forms import CircleForm


def back(request):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@is_authenticated(True)
@is_guest(False)
def settings(request):
    return render(
        request,
        "user/index.html",
        {
            'forms': {
                'info': ProfileInfoForm(instance=request.user.profile),
                'password': PasswordUpdateForm(False),
                'picture': ProfilePictureForm,
                'circle': CircleForm,
                'mate': AccountUsernameForm
            },
            'column': {
                'icon': 'person'
            }
        }
    )

def navigate(request):
    if request.user.is_authenticated:
        if request.user.is_guest:
            return redirect("user:signout")
        else: return redirect("user:settings")
    return redirect("home:index")