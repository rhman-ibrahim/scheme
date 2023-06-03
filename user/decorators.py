from django.shortcuts import redirect
from django.contrib import messages


def is_authenticated(status):
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            if status == request.user.is_authenticated:
                return view(request, *args, **kwargs)
            else:
                if status: messages.warning(request, "you have to signin first.")
                messages.warning(request, "you have to signout first.")
                return redirect('user:navigate')
        return wrapper
    return decorator

def is_guest(status):
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            if status == request.user.is_guest:
                return view(request, *args, **kwargs)
            else:
                if status: messages.warning(request, "Only guest users are allowed to view this.")
                messages.warning(request, "Guest users are not allowed to view this.")
                return redirect('user:navigate')
        return wrapper
    return decorator