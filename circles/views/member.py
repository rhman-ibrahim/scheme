from django.shortcuts import redirect, render
from django.contrib import messages
from user.decorators import is_authenticated
from circles.models import Circle


@is_authenticated(True)
def open(request, serial):

    circle = Circle.objects.get(uuid=serial)
    role   = circle.user_role(request.user)
    
    if 'circle' in request.session:
        if circle.uuid == request.session.get('circle'):
            return redirect("circle:browse")
        else:
            messages.info(request, "close the opened circle")
            return redirect("user:navigate")
    else:
        if role != None:
            request.session['circle'] = circle.uuid
            return redirect("circle:browse")
        else:
            messages.warning(request, "you are not a member")
            return redirect("user:navigate")


@is_authenticated(True)
def browse(request):

    if not 'circle' in request.session:
        return redirect("user:navigate")

    circle = Circle.objects.get(uuid=request.session.get('circle'))
    return render(
        request,
        "circles/index.html",
        {
            'circle': circle
        }
    )


@is_authenticated(True)
def close(request):
    request.session.pop('circle')
    return redirect('user:navigate')