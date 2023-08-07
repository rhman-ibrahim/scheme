# Standard
import cv2, uuid

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
    log
)

# Decorators
from helpers.decorators import back, home
from team.decorators import is_logined
from user.decorators import (
    is_guest, is_expired,
    is_authenticated
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
    uuid_key_8 = str(uuid.uuid4())[:8]
    uuid_key16 = str(uuid.uuid4())[:16]
    Account.objects.create_guest(
        username=uuid_key_8,
        password=uuid_key16
    )
    user = authenticate(
        username=uuid_key_8,
        password=uuid_key16
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
@is_expired
def retrieve_account(request):
    if not request.user.is_guest:
        return render(
            request,
            "user/index.html",
            {
                'forms': {
                    'info': ProfileInfoForm(instance=request.user.profile),
                    'password': PasswordUpdateForm(False),
                    'circle_request': CircleRequestForm,
                    'picture': ProfilePictureForm,
                    'delete': AccountDeleteForm,
                    'mate': AccountUsernameForm,
                    'login': CircleLoginForm,
                    'circle': CircleForm
                },
                'column': {
                    'icon': 'settings'
                }
            }
        )
    return render(
            request,
            "user/guest.html",
            {
                'forms': {
                    'circle_request': CircleRequestForm,
                    'mate': AccountUsernameForm,
                    'login': CircleLoginForm,
                    'circle': CircleForm
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
@is_logined(False)
def update_token(request):
    token = request.user.token
    if token != None:
        token.value = get_random_string(length=32)
        token.save()
        messages.success(request, "your token has been updated successfully")
    return redirect("user:retrieve_account")

@is_authenticated(True)
@is_guest(False)
@is_logined(False)
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
@is_guest(True)
def update_account_status(request):
    account = Account.objects.get(id=request.user.id)
    account.is_active = False
    account.save()
    logout(request)
    messages.info(request, 'Your 8 hours session is over.')
    return redirect("home:render_home_index")

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
            return redirect("home:render_home_index")
        else:
            get_form_errors(request, form)

@is_authenticated(False)
@home
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
    return redirect('home:render_home_index')

@is_authenticated(False)
def verify(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST, request.FILES)
        if form.is_valid():
            path = f'{MEDIA_ROOT}/user/tokens/verify/{get_random_string(length=32)}.png'
            destination = open(path, 'wb+')
            for chunk in request.FILES['token']:
                destination.write(chunk)
            destination.close()
            decoder = cv2.QRCodeDetector()
            reval, point, s_qr, = decoder.detectAndDecode(cv2.imread(path))
            try:
                Token.objects.get(value=reval)
                request.session['token'] = reval
                messages.success(request, "your account has been detected successfully")
            except Token.DoesNotExist:
                messages.error(request, "invalid or used token")
        else:
            get_form_errors(request, form)
    return redirect('home:render_home_index')

@is_authenticated(True)
@is_logined(False)
@home
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
            return redirect("home:render_home_index")
        else:
            messages.error(request, "incorrect password")
    else:
        get_form_errors(request, form)