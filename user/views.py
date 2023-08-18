# Standard
import uuid

# Django
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.admin.models import CHANGE
from django.contrib.auth.hashers import check_password
from django.utils.crypto import get_random_string
from django.shortcuts import redirect, render
from django.contrib.auth import (
    update_session_auth_hash,
    authenticate, login,
    logout,
)

# Scheme
from scheme.settings import MEDIA_ROOT

# Models
from user.models import Account, Token

# Forms
from user.forms import (
    PasswordUpdateForm, AccountDeleteForm,
    VerifyForm, PassWordResetForm,
    SignInForm, SignUpForm
)
from mate.forms import (
    ProfilePictureForm, ProfileInfoForm,
    AccountUsernameForm
)
from team.forms import (
    CircleForm, CircleLoginForm,
    CircleRequestForm
)

# Functions
from helpers.functions import (
    get_form_errors,
    token_reveal,
    log
)

# Decorators
from helpers.decorators import (
    back, center, resource,
    is_guest, is_authenticated,
)

@is_authenticated(False)
def create_account(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "your account has been created successfully."
            )
        else:
            get_form_errors(
                request,
                form
            )
        return redirect("user:retrieve_account")

@is_authenticated(False)
def create_guest(request):
    uuid_key_1 = str(uuid.uuid4())[:8]
    uuid_key_2 = str(uuid.uuid4())[:16]
    Account.objects.create_guest(
        username=uuid_key_1,
        password=uuid_key_2
    )
    user = authenticate(
        username=uuid_key_1,
        password=uuid_key_2
    )
    if user is not None:
        login(
            request,
            user
        )
        log(
            request.user.id,
            request.user,
            CHANGE,
            "signed in as a guest"
        )
    return redirect('user:retrieve_account')

@is_authenticated(True)
def retrieve_account(request):
    return render(
        request,
        "user/index.html",
        {
            'forms': {
                'info': ProfileInfoForm(instance=request.user.profile),
                'password': PasswordUpdateForm(False),
                'circle_request': CircleRequestForm(auto_id="circle_request_%s"),
                'picture': ProfilePictureForm(auto_id="profile_picture_%s"),
                'delete': AccountDeleteForm(auto_id="account_delete_%s"),
                'mate': AccountUsernameForm(auto_id="account_username_%s"),
                'login': CircleLoginForm(auto_id="circle_login_%s"),
                'circle': CircleForm(auto_id="circle_%s")
            },
            'grid': {
                'title': f'.sch | { request.user.username }',
                'icon': 'settings'
            }
        }
    )


@is_authenticated(True)
@is_guest(False)
def retrieve_token(request):
    with open(f"{MEDIA_ROOT}/user/tokens/{request.user.username}.png", 'rb') as f:
        file = f.read()
    response = HttpResponse(content_type='image/png')
    response.write(file)
    return response

@is_authenticated(True)
@is_guest(False)
def update_token(request):
    token = request.user.token
    if token != None:
        token.key = get_random_string(length=32)
        token.save()
        messages.success(request, "your token has been updated successfully")
    return redirect("user:retrieve_account")

@is_authenticated(True)
@is_guest(False)
@back
def update_account_password(request):
    if request.method == 'POST':
        form = PasswordUpdateForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            log(request.user.id, request.user, CHANGE, "updated password")
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

@is_authenticated(False)
@back
def reset_account_password(request):
    if 'token' in request.session and request.method == "POST":
        token = Token.objects.get(value=request.session['token'])
        form = PassWordResetForm(token.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'password has been reset successfully')
            del request.session['token']
            return redirect("home:retrieve_home_index")
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
                log(request.user.id, request.user, CHANGE, "signed in")
                messages.success(request, 'signed in successfully')
                return redirect("user:retrieve_account")
        else:
            get_form_errors(request, form)

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
    return redirect('home:retrieve_home_index')

@is_authenticated(False)
@resource
def token_verify(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST, request.FILES)
        if form.is_valid():
            query = Token.objects.filter(value=token_reveal(request))
            if query.exists() and query.count() == 1:
                request.session['token'] = query.first().value
                messages.success(request, "your account has been detected successfully")
        else:
            get_form_errors(request, form)
    return redirect('home:retrieve_home_index')

@is_authenticated(False)
@resource
def token_signin(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST, request.FILES)
        if form.is_valid():            
            query = Token.objects.filter(value=token_reveal(request))
            if query.exists() and query.count() == 1:
                login(request, query.first().user)
                log(request.user.id, request.user, CHANGE, "signed in using token")
            messages.success(request, 'signed in successfully')
            return redirect("user:retrieve_account")
        else:
            get_form_errors(request, form)
    return redirect('home:retrieve_home_index')

@is_authenticated(True)
@center
def delete_account(request):
    form = AccountDeleteForm(request.POST)
    if form.is_valid():
        if check_password(
            form.cleaned_data['password'], request.user.password
        ):
            account = Account.objects.get(username=request.user.username)
            account.delete()
            messages.success(
                request,
                "your account has been deleted successfully."
            )
            logout(request)
            return redirect("home:retrieve_home_index")
        else:
            messages.error(request, "incorrect password")
    else:
        get_form_errors(request, form)