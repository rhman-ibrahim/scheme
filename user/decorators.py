from django.shortcuts import redirect
from django.contrib import messages


def activated(view):
    def wrapper(request, *args, **kwargs):
        if request.user.is_active:
            return view(request, *args, **kwargs)
        messages.warning(request, 'your account is not activated')
        return redirect("user:navigate")
    return wrapper

def superuser(view):
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return view(request, *args, **kwargs)
        messages.warning(request, 'you are not authorized to view this')
        return redirect("user:navigate")
    return wrapper

def authentication(status):
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            if status == request.user.is_authenticated:
                return view(request, *args, **kwargs)
            else:
                if status:
                    messages.warning(request, "you have to signin first.")
                else:
                    messages.warning(request, "you have to signout first.")
                return redirect('user:navigate')
        return wrapper
    return decorator

def guest(allowed):
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            if allowed:
                if request.user.is_authenticated and request.user.is_lazy:
                    return view(request, *args, **kwargs)
                else:
                    messages.warning(request, "This is a guest account, signup first.")
            return redirect('user:navigate')
        return wrapper
    return decorator