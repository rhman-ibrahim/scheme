# Response
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db.models import Q

# Decorators
from user.decorators import is_authenticated, is_guest

# Models
from team.models import Circle, CircleRequest

# Forms
from mate.forms import ProfilePictureForm, ProfileInfoForm, AccountUsernameForm
from user.forms import PasswordUpdateForm, AccountDeleteForm
from team.forms import CircleForm, CircleLoginForm


def nav(request):
    if request.user.is_authenticated:
        if request.user.is_guest:
            return redirect("user:guest")
        return redirect("user:settings")
    return redirect("home:index")

@is_authenticated(True)
@is_guest(True)
def guest(request):
    circle_query  = Circle.objects.filter(Q(founder=request.user)|Q(members=request.user))
    request_query = CircleRequest.objects.filter(user=request.user)
    guest_type    = "inactive"
    if circle_query.exists():
        circle     = circle_query.first()
        guest_type = circle.user_role(request.user)
    if request_query.exists():
        circle_request = request_query.first()
        guest_type     = "requester"
    return render(
            request,
            "user/guest.html",
            {
                'guest': {
                    'request': circle_request if request_query.exists() else None,
                    'circle': circle if circle_query.exists() else None,
                    'type': guest_type
                },
                'form': {
                    'login': CircleLoginForm
                }

            }
        )

@is_authenticated(True)
@is_guest(False)
def settings(request):
    return render(
        request,
        "user/index.html",
        {
            'forms': {
                'delete': AccountDeleteForm(),
                'info': ProfileInfoForm(instance=request.user.profile),
                'password': PasswordUpdateForm(False),
                'picture': ProfilePictureForm,
                'mate': AccountUsernameForm,
                'login': CircleLoginForm,
                'circle': CircleForm
            },
            'column': {
                'icon': 'person'
            }
        }
    )

def back(request):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))