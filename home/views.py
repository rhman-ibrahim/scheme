# Django
from django.contrib import messages
from django.contrib.auth import (
    authenticate, login,
)
from django.shortcuts import (
    render, redirect
)

# Models
from user.models import Token
from team.models import Membership

# Forms
from team.forms import SpaceForm
from mate.forms import SignalForm
from .forms import (
    SignUpForm, SignInForm,
    PassWordResetForm,
    KeyForm
)

# Helpers
from helpers.decorators import (
    is_authenticated, resource, back
)
from helpers.functions import (
    get_form_errors, create_a_temporary_account
)


@is_authenticated(False)
def sign(request):
    create_a_temporary_account(request)
    return redirect('user:account')
    
@is_authenticated(False)
@back
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"your account has been created successfully.")
        else:
            get_form_errors(request,form)

@is_authenticated(False)
@back
def sign_in(request):
    if request.method == 'POST':
        form = SignInForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, 'signed in successfully')
            return redirect("user:account")
        else:
            get_form_errors(request, form)

@is_authenticated(False)
@resource
def account(request):
    if request.method == 'POST':
        form = KeyForm(request.POST)
        if form.is_valid():            
            query = Token.objects.filter(key=form.cleaned_data['key'])
            if query.exists() and query.count() == 1:
                login(request, query.first().user)
            messages.success(request, 'signed in successfully')
            return redirect("user:account")
        else:
            get_form_errors(request, form)
    return redirect('home:index')

@resource
def space(request):
    if request.method == 'POST':
        form = KeyForm(request.POST)
        if form.is_valid():
            token = Membership.objects.get(key=form.cleaned_data['key'])
            messages.success(request,"your membership has been verified successfully")
            request.session['space'] = token.space.id
            if not request.user.is_authenticated:
                login(request, token.user)
            return redirect("team:index")
        else:
            get_form_errors(request, form)


@is_authenticated(False)
@back
def reset(request):
    if request.method == "POST":
        token = Token.objects.get(key=request.POST['key'])
        form = PassWordResetForm(token.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'password has been reset successfully')
            return redirect("home:index")
        else:
            get_form_errors(request, form)

@is_authenticated(False)
@resource
def index(request):
    return render(
        request,
        "home/index.html",
        {
            'grid': {
                'title': "Express on your behalf or anonymously.",
            },
            'forms': {
                'user': {
                    'signup': SignUpForm(auto_id="sign_up_%s"),
                    'signin': SignInForm(auto_id="sign_in_%s"),
                },
                'note': {
                    'reset': PassWordResetForm(False, auto_id="password_reset_%s"),
                    'signin': KeyForm(auto_id=f"sign_in_with_token_%s"),
                    'login': KeyForm(auto_id=f"login_secret_%s")
                },
                'mate': {
                    'friend': {
                        'request':SignalForm(auto_id="friend_request_%s"),
                    },
                    'space': {
                        'request': SignalForm(auto_id="space_request_%s")
                    }
                },
                'team': {
                    'space': SpaceForm(auto_id="space_form_%s")
                }
            }
        }
    )

def object_not_found(request):
    return render(
        request,
        "home/404.html",
        {
            'grid': {
                'title': "404 Object Is Not Found",
            },
        }
    )