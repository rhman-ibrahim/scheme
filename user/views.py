# Django
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect, render
from django.contrib.auth import (
    update_session_auth_hash,
    authenticate, login,
    logout,
)

# Models
from .models import Account

# Forms
from mate.forms import SignalForm
from team.forms import SpaceForm, SpaceLoginForm
from note.forms import KeyForm
from .forms import (
    SignInForm, SignUpForm,
    PasswordUpdateForm, ProfileForm,
    PasswordForm
)

# Functions
from helpers.functions import (
    get_form_errors,
    create_a_guest_account,
)

# Decorators
from helpers.decorators import (
    is_guest, is_authenticated,
    back, center, resource,
)


@is_authenticated(False)
def create_account(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"your account has been created successfully.")
        else:
            get_form_errors(request,form)
        return redirect("user:retrieve_account")

@is_authenticated(False)
def create_guest(request):
    create_a_guest_account(request)
    return redirect('user:retrieve_account')

@is_authenticated(True)
def retrieve_account(request):
    return render(
        request,
        "user/index.html",
        {
            'grid': {
                'title': f'Settings / { request.user.username }',
                'icons': {
                    'left': 'layers',
                    'right': 'menu'
                }
            },
            'forms': {
                'user': {
                    'password': PasswordUpdateForm(False),
                    'delete': PasswordForm(auto_id="account_delete_%s"),
                    'info': ProfileForm(instance=request.user.profile, auto_id="profile_info_%s"),
                },
                'team': {
                    'space': SpaceForm(auto_id="space_%s"),
                    'login': SpaceLoginForm(auto_id="space_login_%s")
                },
                'note': {
                    'login': KeyForm(auto_id="space_login_%s")
                },
                'mate': {
                    'friend': {
                        'request':SignalForm(auto_id="friend_request_%s")
                    },
                    'space': {
                        'request': SignalForm(auto_id="space_request_%s")
                    }
                }
            }
        }
    )

@is_authenticated(True)
@is_guest(False)
@back
def update_account_password(request):
    if request.method == 'POST':
        form = PasswordUpdateForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'password has been updated successfully')
        else:
            get_form_errors(request, form)


@is_authenticated(True)
@resource
def update_account_status(request):
    account = Account.objects.get(id=request.user.id)
    account.is_active = False
    account.save()
    logout(request)
    messages.info(request, 'account has been deactivated')
    return redirect("home:retrieve_home_index")

@is_authenticated(True)
@is_guest(False)
@back
def update_profile_info(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form         = form.save(commit=False)
            form.account = request.user
            form.save()
            messages.success(request, "profile info updated successfully")
        else:
            get_form_errors(request, form)

@is_authenticated(False)
@center
def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                messages.success(request, 'signed in successfully')
                return redirect("user:retrieve_account")
        else:
            get_form_errors(request, form)

@is_authenticated(True)
def signout(request):
    if 'circle' in request.session:
        request.session.pop('circle')
    logout(request)
    messages.success(request, 'signed out successfully')
    return redirect('home:retrieve_home_index')

@is_authenticated(True)
@center
def delete_account(request):
    form = PasswordForm(request.POST)
    if form.is_valid():
        if check_password(form.cleaned_data['password'],request.user.password):
            account = Account.objects.get(username=request.user.username)
            account.delete()
            messages.success(request,"your account has been deleted successfully.")
            logout(request)
            return redirect("home:retrieve_home_index")
        else:
            messages.error(request,"incorrect password")
    else:
        get_form_errors(request, form)