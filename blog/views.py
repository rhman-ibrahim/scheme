# Django
from django.shortcuts import render, redirect
from django.contrib import messages

# Models
from team.models import Circle
from ping.models import Room
from .models import Signal

# Forms
from .forms import SignalForm

# Decorators
from helpers.decorators import back

# Funtions
from helpers.functions import get_form_errors


# Create

@back
def create_signal(request):
    if request.method == "POST":
        form = SignalForm(request.POST)
        if form.is_valid():
            signal        = form.save(commit=False)
            signal.circle = Circle.objects.get(id=request.session.get('circle'))
            if 'parent_signal_id' in request.session:
                messages.info(request, "OMG")
                # parent        = Signal.objects.get(id=request.session.get('parent_signal_id')) 
                # signal.parent = parent
                # signal.owner  = parent.user
            signal.owner  = request.user
            signal.user   = request.user
            form.save()
            messages.success(request, "your signal has been sent successfully")
        else:
            get_form_errors(request, form)

# Retieve

def retrieve_signal(request, serial):
    signal = Signal.objects.get(serial=serial)
    request.session['parent_signal_id'] = signal.id
    return render(
        request,
        "blog/index.html",
        {
            'signal': signal,
            'room': Room.objects.get(serial=signal.serial),
            'forms': {
                'signal' : SignalForm
            },
            'icons': {
                'left':"diversity_2",
                "right":"forum"
            }
        }
    )

# Update

def update_signal_status(request, serial):
    query = Signal.objects.filter(serial=serial)
    if query.exsits() and query.count() == 1:
        signal = query.first()
        signal.status = False if signal.status else True
        signal.save()
        return redirect("ping:update_room_status", signal.serial)
    else:
        messages.warning(request, "something has gone wrong")
    return redirect("blog:detail", signal.serial)