from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import redirect
from django.contrib import messages


def home(view):
    def wrapper(request, *args, **kwargs):
        view(request, *args, **kwargs)
        if request.user.is_authenticated:
            if request.user.is_guest:
                return redirect("user:retrieve_account")
            return redirect("user:retrieve_account")
        return redirect("home:render_home_index")
    return wrapper

def back(view):
    def wrapper(request, *args, **kwargs):
        response = view(request, *args, **kwargs)
        if not isinstance(response, (HttpResponseRedirect, HttpResponsePermanentRedirect)):
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return response
    return wrapper

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