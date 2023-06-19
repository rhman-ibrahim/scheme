# Django
from django.shortcuts import render, redirect
from django.contrib import messages
# Helpers
from helpers.functions import get_form_errors
# Circles
from circles.models import Circle
from circles.decorators import circle_session
# Signals
from .forms.signal import SignalForm
from .models import Signal


@circle_session
def create_problem(request):
    if  request.method == "POST":
        form = SignalForm(request.POST)
        if form.is_valid():
            signal                = form.save(commit=False)
            signal.circle         = Circle.objects.get(serial=request.session.get('circle'))
            signal.classification = 0
            signal.owner          = request.user
            signal.user           = request.user
            signal.icon           = "psychology_alt"
            form.save()
            messages.success(request, "your signal has been sent successfully")
        else: get_form_errors(request, form)
    return redirect("home:back")

@circle_session
def create_opportunity(request):
    if  request.method == "POST":
        form = SignalForm(request.POST)
        if form.is_valid():
            signal                = form.save(commit=False)
            signal.circle         = Circle.objects.get(serial=request.session.get('circle'))
            signal.classification = 1
            signal.owner          = request.user
            signal.user           = request.user
            signal.icon           = "psychology"
            form.save()
            messages.success(request, "your signal is sent successfully")
        else: get_form_errors(request, form)
    return redirect("home:back")

@circle_session
def create_hypothesis(request):
    if  request.method == "POST":
        form = SignalForm(request.POST)
        if form.is_valid():
            signal                = form.save(commit=False)
            signal.circle         = Circle.objects.get(serial=request.session.get('circle'))
            signal.classification = 2
            signal.owner          = form.cleaned_data['parent'].owner
            signal.user           = request.user
            signal.icon           = "cognition"
            form.save()
            messages.success(request, "your signal is sent successfully")
        else: get_form_errors(request, form)
    return redirect("home:back")

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
    signal.status = 0 if signal.status else 1
    signal.save()
    return redirect("home:back")


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
                'hypothesis' : SignalForm(
                    initial = {
                        'parent' : signal
                    }
                )
            }
        }
    )