from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import redirect
from django.contrib import messages
from team.models import Circle


def center(view):
    def wrapper(request, *args, **kwargs):
        view(request, *args, **kwargs)
        if request.user.is_authenticated:
            return redirect("user:retrieve_account")
        return redirect("home:retrieve_home_index")
    return wrapper

def resource(view):
    def wrapper(request, *args, **kwargs):
        try:
            return view(request, *args, **kwargs)
        except ObjectDoesNotExist:
            messages.warning(request, "the requested resource does not exist")
            return redirect('home:resource_not_found')
    return wrapper

def back(view):
    @resource
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
                    return redirect("home:retrieve_home_index")
                else:
                    messages.warning(request, "you have to sign-out first.")
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
                    messages.warning(request, "only guest users are allowed.")
                messages.warning(request, "guest users are not allowed.")
                return redirect('user:retrieve_account')
        return wrapper
    return decorator

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
    
def is_founder(view):
    def wrapper(request, *args, **kwargs):
        if 'circle' in request.session:
            query = Circle.objects.filter(id=request.session.get('circle'))
            if query.exists():
                circle = query.first()
                if circle.founder == request.user:
                    return view(request, *args, **kwargs)
                else:
                    messages.warning(
                        request,
                        "only circle founder is allowed"
                    )
                    return redirect('team:retrieve_team_index')
        return wrapper