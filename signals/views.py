from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from helpers.functions import get_form_errors
from .models import Signal, Note, Comment
from .forms import SignalForm, CommentForm, NoteForm


def index(request):
    return render(
        request,
        "signals/index.html",
        {
            "signal": {
                'list': Signal.objects._mptt_filter(level=0),
                "forms": {
                    'idea': SignalForm,
                }
            }
        }
    )

def create_signal(request):
    if  request.method == "POST":
        form = SignalForm(request.POST)
        if form.is_valid():
            signal      = form.save(commit=False)
            signal.user = request.user
            form.save()
            messages.success(request, "your signal is created successfully")
        else: get_form_errors(request, form)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def create_note(request):
    if  request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note      = form.save(commit=False)
            note.user = request.user
            form.save()
            messages.success(request, "your note is created successfully")
        else: get_form_errors(request, form)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def create_comment(request):
    if  request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment      = form.save(commit=False)
            comment.user = request.user
            form.save()
            messages.success(request, "your comment is created successfully")
        else: get_form_errors(request, form)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def read_idea(request, id):
    signal = Signal.objects.get(serial=id)
    return render(
        request,
        "signals/idea.html",
        {
            "idea": {
                'object': signal,
            },
            "signal": {
                "forms": {
                    'concern': SignalForm(initial={'parent':signal}),
                }
            }
        }
    )

def read_concern(request, id):
    concern = Signal.objects.get(serial=id)
    return render(
        request,
        "signals/concern.html",
        {
            "concern": {
                'object': concern,
            },
            "signal": {
                "forms": {
                    'test': SignalForm(initial={'parent':concern}),
                }
            }
        }
    )

def read_test(request, id):
    test = Signal.objects.get(serial=id)
    return render(
        request,
        "signals/test.html",
        {
            "test": {
                'object': test,
            },
            "signal": {
                "forms": {
                    'result': SignalForm(initial={'parent':test})
                }
            }
        }
    )

def read_result(request, id):
    result = Signal.objects.get(serial=id)
    return render(
        request,
        "signals/result.html",
        {
            "result": {
                "object": result,
            },
        }
    )

def update_signal(request, id):
    if request.method == "POST":
        form = SignalForm(request.POST, instance=Signal.objects.get(serial=id))
        if form.is_valid():
            form.save()
            messages.success(request, "your signal is updated successfully")
        else: get_form_errors(request, form)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def update_comment(request, id):
    if request.method == "POST":
        form = CommentForm(request.POST, instance=Comment.objects.get(serial=id))
        if form.is_valid():
            form.save()
            messages.success(request, "your comment is updated successfully")
        else: get_form_errors(request, form)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delete_signal(request, id):
    Signal.objects._mptt_filter(serial=id).delete()
    messages.success(request, "your signal is deleted successfully")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delete_comment(request, id):
    Comment.objects._mptt_filter(id=id).delete()
    messages.success(request, "your comment is deleted successfully")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))