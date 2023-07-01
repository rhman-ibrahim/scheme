# Django
from django.shortcuts import render, redirect
from django.contrib import messages
# Helpers
from helpers.functions import get_form_errors
# Circles
from circles.models import Circle
from circles.decorators import circle_session
# Spaces
from spaces.models import Room
# Signals
from .forms.signal import SignalForm
from .models import Signal


@circle_session
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

@circle_session
def list(request):
    circle  = Circle.objects.get(serial=request.session.get('circle'))
    signals = Signal.objects.filter(circle=circle, classification__lte=1).order_by('-created')
    return render(
        request,
        "signals/index.html",
        {
            'list': signals,
            "forms": {
                'signal': SignalForm,
            }
        }
    )

def update_status(request, serial):
    signal        = Signal.objects.get(serial=serial)
    room          = Room.objects.get(space=serial)
    signal.status = 0 if signal.status else 1
    room.status = signal.status
    signal.save()
    room.save()
    return redirect("user:back")


@circle_session
def detail(request, serial):
    signal = Signal.objects.get(serial=serial)
    return render(
        request,
        "signals/signal.html",
        {
            'signal': signal,
            'room_serial': signal.serial,
            'forms': {
                'signal' : SignalForm(
                    initial = {
                        'parent' : signal
                    }
                )
            }
        }
    )