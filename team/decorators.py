from django.contrib import messages
from django.shortcuts import redirect
from helpers.decorators import back

from django.db.models import Q
from team.models import Circle, CircleRequest

def is_logined(status):
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            connected = True if 'circle' in request.session else False
            if request.user.is_authenticated:
                if status == connected:
                    return view(request, *args, **kwargs)
                elif status == True:
                    messages.warning(request, "you have to login to the circle.")
                else:
                    messages.warning(request, "you have to logout to the circle.")
                    return redirect('team:retrieve_team_index')
            messages.warning(request, "you have to signin")
        return wrapper
    return decorator

def is_connected(view):
    def wrapper(request, *args, **kwargs):
        if request.user.is_guest:
            c = Circle.objects.filter(
                Q(founder=request.user) |
                Q(members=request.user)
            )
            r = CircleRequest.objects.filter(
                Q(user=request.user) &
                ~Q(status=0)
            )
            if c.exists() or r.exists():
                messages.info(
                    request,
                    "as a guest you can communicate only with 1 circle"
                )
                return redirect("user:retrieve_account")
            else:
                return view(request, *args, **kwargs)
        return wrapper