from django.contrib import messages
from django.shortcuts import redirect


def is_logined(status):
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            connected = True if 'circle' in request.session else False
            if request.user.is_authenticated:
                if status == connected:
                    return view(request, *args, **kwargs)
                elif status == True:
                    messages.warning(request, "you have to login to the circle.")
                    return redirect('user:back')
                else:
                    messages.warning(request, "you have to logout to the circle.")
                    return redirect('team:browse')
            messages.warning(request, "you have to signin")
            return redirect('user:back')
        return wrapper
    return decorator