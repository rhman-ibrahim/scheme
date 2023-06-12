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
from .models import Problem, Opportunity


@circle_session
def create_problem(request):
    if  request.method == "POST":
        form = SignalForm(request.POST)
        if form.is_valid():
            problem        = Problem(**form.cleaned_data)
            problem.author = request.user
            problem.circle = Circle.objects.get(uuid=request.session.get('circle'))
            problem.save()
            messages.success(request, "your signal has been sent successfully")
        else: get_form_errors(request, form)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@circle_session
def create_opportunity(request):
    if  request.method == "POST":
        form = SignalForm(request.POST)
        if form.is_valid():
            opportunity        = Opportunity(**form.cleaned_data)
            opportunity.author = request.user
            opportunity.circle = Circle.objects.get(uuid=request.session.get('circle'))
            opportunity.save()
            messages.success(request, "your signal is sent successfully")
        else: get_form_errors(request, form)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@circle_session
def index(request):

    circle        = Circle.objects.get(uuid=request.session.get('circle'))
    opportunities = Opportunity.objects._mptt_filter(circle=circle)
    problems      = Problem.objects._mptt_filter(circle=circle)

    combined_list = list(chain(opportunities, problems))
    signals       = sorted(combined_list, key=attrgetter('created'))

    return render(
        request,
        "signals/index.html",
        {
            "hypothesis": {
                'list': signals,
            },
            "forms": {
                'signal': SignalForm,
            }
        }
    )