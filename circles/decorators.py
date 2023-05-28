# Django
from django.shortcuts import redirect
from django.contrib import messages

# Circles
from .models import Circle


def circle(view):
    def decorator(request, *args, **kwargs):
        if request.user.is_authenticated:
            if 'circle' not in request.session:
                messages.warning(request, "there is no opened circle's session.")
                return redirect("user:navigate")
        return redirect("user:navigate")
    return decorator

def founder(view):
    def decorator(request, *args, **kwargs):
        circle = Circle.objects.get(id=request.session['circle'])
        if request.user.is_authenticated and request.user == circle.founder:
            return view(request, *args, **kwargs)
        messages.warning(request, "you are not authorized to view this.")
        return redirect("user:navigate")
    return decorator

def member(view):
    def decorator(request, *args, **kwargs):
        circle = Circle.objects.get(id=request.session['circle'])
        if request.user.is_authenticated:
            if request.user == circle.founder or request.user in circle.members.all():
                return view(request, *args, **kwargs)
        messages.warning(request, "you are not authorized to view this.")
        return redirect("user:navigate")
    return decorator