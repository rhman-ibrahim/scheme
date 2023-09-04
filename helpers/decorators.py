from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import redirect
from django.contrib import messages
from team.models import Space


def center(view):
    def wrapper(request, *args, **kwargs):
        view(request, *args, **kwargs)
        if request.user.is_authenticated:
            return redirect("user:account")
        return redirect("home:index")
    return wrapper

def resource(view):
    def wrapper(request, *args, **kwargs):
        try:
            return view(request, *args, **kwargs)
        except ObjectDoesNotExist:
            messages.warning(request, "the requested resource does not exist")
            return redirect('home:404')
    return wrapper

def back(view):
    # @resource
    def wrapper(request, *args, **kwargs):
        response = view(request, *args, **kwargs)
        if not isinstance(response, (HttpResponseRedirect, HttpResponsePermanentRedirect)):
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return response
    return wrapper

def is_authenticated(status):
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            if status == request.user.is_authenticated:
                return view(request, *args, **kwargs)
            else:
                if status:
                    messages.warning(request, "you have to sign-in first.")
                    return redirect("home:index")
                else:
                    messages.warning(request, "you have to sign-out first.")
                    return redirect("user:account")
        return wrapper
    return decorator

def is_temporary(status):
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            if status == request.user.is_temporary:
                return view(request, *args, **kwargs)
            else:
                if status == True:
                    messages.warning(request, "only guest users are allowed.")
                else:
                    messages.warning(request, "guest users are not allowed.")
                    return redirect('user:account')
        return wrapper
    return decorator

def is_logged(status):
    def decorator(view):
        @is_authenticated(True)
        def wrapper(request, *args, **kwargs):
            connection = True if 'space' in request.session else False
            if status == connection:
                return view(request, *args, **kwargs)
            else:
                if status == True:
                    messages.warning(request, "you have to login to the space.")
                else:
                    messages.warning(request, "you have to logout to the space.")
                return redirect('team:index')
        return wrapper
    return decorator
    
def is_founder(view):
    @is_authenticated(True)
    @is_logged(True)
    def wrapper(request, *args, **kwargs):
        query = Space.objects.filter(id=request.session.get('space'))
        if query.exists():
            space = query.first()
            if space.founder == request.user:
                return view(request, *args, **kwargs)
            else:
                messages.warning(
                    request,
                    "only space founder is allowed"
                )
                return redirect('team:index')
    return wrapper