from django.contrib import messages
from django.shortcuts import redirect
from team.processors import opened_circle


def circle_session(view):
    def decorator(request, *args, **kwargs):
        if 'circle' in request.session:
            return view(request, *args, **kwargs)
        else:
            messages.warning(request, "there is no opened circle")
            return redirect('user:navigate')
    return decorator