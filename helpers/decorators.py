from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.contrib import messages


def resource(link):
    # Check if the resource exists.
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            try:
                return view(request, *args, **kwargs)
            except ObjectDoesNotExist:
                messages.warning(request, "the requested resource does not exist")
                return redirect(link)
        return wrapper
    return decorator