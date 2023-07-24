# Django
from django.shortcuts import render, redirect
from django.contrib import messages
# Helpers
from helpers.functions import get_form_errors
# Team
from team.models import Circle
# Ping
from ping.models import Room
# Blog
from .forms import SignalForm
from .models import Signal


def create_signal(request):
    if  request.method == "POST":
        form = SignalForm(request.POST)
        if form.is_valid():
            signal                = form.save(commit=False)
            signal.circle         = Circle.objects.get(serial=request.session.get('circle'))
            signal.classification = request.POST['classification']
            signal.icon           = request.POST['icon']
            signal.owner          = request.user
            signal.user           = request.user
            form.save()
            messages.success(request, "your signal has been sent successfully")
        else: get_form_errors(request, form)
    return redirect("user:back")

def update_status(request, serial):
    signal        = Signal.objects.get(serial=serial)
    room          = Room.objects.get(serial=serial)
    signal.status = 0 if signal.status else 1
    room.status = signal.status
    signal.save()
    room.save()
    return redirect("user:back")
    
def detail(request, serial):
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