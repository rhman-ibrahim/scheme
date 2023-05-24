from django.shortcuts import redirect
from django.contrib import messages


def superuser(view):
    # Check if the user is a superuser.
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return view(request, *args, **kwargs)
        messages.warning(request, 'you are not authorized to view this')
        return redirect("user:settings")
    return wrapper

def authenticated(status):
    # Check if the user is authenticated.
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            if status == request.user.is_authenticated:
                return view(request, *args, **kwargs)
            if status:
                messages.warning(request, "you have to signin first.")
                return redirect('home:user')
            messages.warning(request, "you have to signouty first.")
            return redirect("user:settings")
        return wrapper
    return decorator

def activated(view):
    # Check if the user is activated.
    def wrapper(request, *args, **kwargs):
        if request.user.is_active:
            return view(request, *args, **kwargs)
        messages.warning(request, 'your account is not activated')
        return redirect("user:settings")
    return wrapper