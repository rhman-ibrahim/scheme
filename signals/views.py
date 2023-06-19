from itertools import chain
from operator import attrgetter
# Django
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
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
            signal.circle         = Circle.objects.get(uuid=request.session.get('circle'))
            signal.classification = 0
            signal.author         = request.user
            signal.icon           = "psychology_alt"
            form.save()
            messages.success(request, "your signal has been sent successfully")
        else: get_form_errors(request, form)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@circle_session
def create_opportunity(request):
    if  request.method == "POST":
        form = SignalForm(request.POST)
        if form.is_valid():
            signal                = form.save(commit=False)
            signal.circle         = Circle.objects.get(uuid=request.session.get('circle'))
            signal.classification = 1
            signal.author         = request.user
            signal.icon           = "psychology"
            form.save()
            messages.success(request, "your signal is sent successfully")
        else: get_form_errors(request, form)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@circle_session
def create_hypothesis(request):
    if  request.method == "POST":
        form = SignalForm(request.POST)
        if form.is_valid():
            signal                = form.save(commit=False)
            signal.circle         = Circle.objects.get(uuid=request.session.get('circle'))
            signal.classification = 2
            signal.author         = request.user
            signal.icon           = "cognition"
            form.save()
            messages.success(request, "your signal is sent successfully")
        else: get_form_errors(request, form)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@circle_session
def list(request):
    circle  = Circle.objects.get(uuid=request.session.get('circle'))
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