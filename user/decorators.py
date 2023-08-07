from django.shortcuts import redirect
from django.contrib import messages


def is_authenticated(status):
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            if status == request.user.is_authenticated:
                return view(request, *args, **kwargs)
            else:
                if status:
                    messages.warning(request, "you have to signin first.")
                    return redirect("home:render_home_index")
                else:
                    messages.warning(request, "you have to signout first.")
                    return redirect("user:retrieve_account")
        return wrapper
    return decorator

def is_guest(status):
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            if status == request.user.is_guest:
                return view(request, *args, **kwargs)
            else:
                if status:
                    messages.warning(request, "Only guest users are allowed to view this.")
                messages.warning(request, "Guest users are not allowed to view this.")
                return redirect('user:retrieve_account')
        return wrapper
    return decorator

def is_expired(view):
    def wrapper(request, *args, **kwargs):
        if request.user.is_guest:
            termination = request.user.termination
            if termination['state']:
                return redirect("user:terminate")
        return view(request, *args, **kwargs)
    return wrapper