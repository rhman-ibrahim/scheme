# Django
from django.shortcuts import render, redirect
from django.contrib import messages

# Helpers
from helpers.functions import get_form_errors

# Models
from team.models import Circle
from ping.models import Room
from .models import Signal

# Forms
from .forms import SignalForm


def create_signal(request):
    if  request.method == "POST":
        form = SignalForm(request.POST)
        if form.is_valid():
            signal                = form.save(commit=False)
            signal.circle         = Circle.objects.get(id=request.session.get('circle'))
            signal.owner          = request.user
            signal.user           = request.user
            form.save()
            messages.success(request, "your signal has been sent successfully")
        else: get_form_errors(request, form)
    return redirect("user:back")

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
    
def get_signal(request, serial):
    signal = Signal.objects.get(serial=serial)
    return render(
        request,
        "blog/signal.html",
        {
            'forms': {
                'signal' : SignalForm(
                    initial = {
                        'parent' : signal
                    }
                )
            },
            'icons': {
                'left':"diversity_2",
                "right":"forum"
            },
            'signal': signal,
            'room': Room.objects.get(serial=signal.serial),
        }
    )