# Django
from django.contrib import messages
from django.contrib.admin.models import CHANGE
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
# Helpers
from helpers.functions import log, get_form_errors
# User
from user.forms import SignUpForm, SignInForm
from user.decorators import is_authenticated

def end_token_session(request):
    if 'token' in request.session:
        del request.session['token']

@is_authenticated(False)
def signup(request):
    end_token_session(request)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "your account has been created successfully.")
        else:
            get_form_errors(request, form)
        return redirect("user:back")

@is_authenticated(False)    
def signin(request):
    end_token_session(request)
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                log(request.user.id, request.user, CHANGE, "signed in")
                messages.success(request, 'signed in successfully')
                return redirect("user:settings")
        else:
            get_form_errors(request, form)
    return redirect("user:back")

@is_authenticated(True)
def signout(request):
    if 'circle' in request.session:
        request.session.pop('circle')
    log(
        request.user.id,
        request.user,
        CHANGE, 
        "signed out"
    )
    logout(request)
    messages.success(request, 'signed out successfully')
    return redirect('home:index')