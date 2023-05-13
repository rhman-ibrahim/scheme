import uuid
import cv2
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.contrib.auth import (
    authenticate, login, logout,
    update_session_auth_hash
)
from django.contrib.admin.models import LogEntry, CHANGE, DELETION
from django.contrib import messages
from scheme.settings import MEDIA_ROOT
from user.decorators import authenticated, superuser
from user.models import Account, Token
from user.forms import (
    SignUpForm, SignInForm, TokenForm, ProfilePictureForm,
    PasswordUpdateForm, ProfileInfoForm, PassWordResetForm
)
from helpers.functions import get_form_errors, log
from helpers.decorators import resource



# Templates

## Anonymous

@authenticated(False)
def index(request):
    return render(
        request,
        "user/index.html",
        {
            'forms': {
                'signup': SignUpForm,
                'signin': SignInForm,
                'token': TokenForm
            }
        }
    )

## Identified

def identified(request):
    token = Token.objects.get(value=request.session['token'])
    if 'token' in request.session:
        return render(
            request,
            "user/identified.html",
            {
                'user': token.user,
                'logs': LogEntry.objects.filter(user_id=token.user.id),
                'forms': {
                    'reset': PassWordResetForm(token.user),
                    'signup': SignUpForm,
                    'signin': SignInForm,
                }
            }
        )
    return redirect('user:index')

## Authenticated

@authenticated(True)
def settings(request):
    return render(
        request,
        "user/settings.html",
        {
            'logs': LogEntry.objects.filter(user_id=request.user.id),
            'forms': {
                'picture': ProfilePictureForm,
                'password': PasswordUpdateForm(False),
                'info': ProfileInfoForm(instance=request.user.profile)
            },
            'state': {
                'profile': True if request.user.profile.completion_percentage == 1 else False,
                'super_user': True if request.user.is_superuser == 1 else False
            }
        }
    )

# Forms
## Anonymous

@authenticated(False)
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, "your account has been created successfully.")
        else: get_form_errors(request, form)
        return redirect("user:index")

@authenticated(False)
def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                log(request.user.id, request.user, CHANGE, "signed in")
                messages.success(request, 'signed in successfully')
                return redirect("user:settings")
        else: get_form_errors(request, form)
    return redirect("user:index")

def verify(request):
    if request.method == 'POST':
        # upload the data file
        form = TokenForm(request.POST, request.FILES)
        if form.is_valid():
            # define a path
            path = f'{MEDIA_ROOT}/user/account/verify/{get_random_string(length=32)}.png'
            # open this path as an empty file
            # copy each chunk from uploaded file to the empty file
            # close that file after writing
            destination = open(path, 'wb+')
            for chunk in request.FILES['token']: destination.write(chunk)
            destination.close()
            # load decoder
            decoder = cv2.QRCodeDetector()
            # then decode QR code
            reval, point, s_qr, = decoder.detectAndDecode(cv2.imread(path))
            try:
                # check if it's a valid user's token
                Token.objects.get(value=reval)
                # then open a session
                request.session['token'] = reval
                messages.success(request, "your account has been detected successfully")
            except Token.DoesNotExist:
                messages.error(request, "invalid or used token")
        else: get_form_errors(request, form)
    return redirect('user:identified')

## Identified

def reset(request):
    if 'token' in request.session and request.method == "POST":
        token = Token.objects.get(value=request.session['token'])
        form = PassWordResetForm(token.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'password has been reset successfully')
            return redirect('user:token')
        else: get_form_errors(request, form)
    return redirect('user:index')

def cancel(request):
    if 'token' in request.session: del request.session['token']
    return redirect("user:index")

## Authenticated

@authenticated(True)
def update_profile_picture(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form         = form.save(commit=False)
            form.account = request.user
            form.save()
            log(request.user.id, request.user, CHANGE, "updated profile picture")
            messages.success(request, "profile picture updated successfully")
        else: get_form_errors(request, form)
    return redirect('user:index')

@authenticated(True)
def update_password(request):
    if request.method == 'POST':
        form = PasswordUpdateForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            log(request.user.id, request.user, CHANGE, "updated password")
            messages.success(request, 'password has been updated successfully')
            return redirect("user:index")
        else: get_form_errors(request, form)
    return redirect('user:index')

@authenticated(True)
def update_profile_info(request):
    if request.method == 'POST':
        form = ProfileInfoForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form         = form.save(commit=False)
            form.account = request.user
            form.save()
            log(request.user.id, request.user, CHANGE, "updated profile info")
            messages.success(request, "profile info updated successfully")
        else: get_form_errors(request, form)
    return redirect('user:settings')

# Functionalities

def navigate(request):
    if request.user.is_authenticated: return redirect("user:settings")
    return redirect("user:index")

## Anonymous

@authenticated(False)
def lazy_signup(request):
    uuid_key_8 = str(uuid.uuid4())[:8]
    uuid_key16 = str(uuid.uuid4())[:16]
    Account.objects.create_lazy_user(username=uuid_key_8, password=uuid_key16)
    user = authenticate(username=uuid_key_8, password=uuid_key16)
    if user is not None:
        login(request, user)
        log(request.user.id, request.user, CHANGE, "signed in as a user")
    return redirect("user:settings")

## Authenticated

@authenticated(True)
def signout(request):
    log(request.user.id, request.user, CHANGE, "signed out")
    logout(request)
    messages.success(request, 'signed out successfully')
    return redirect('user:index')


def token(request):
    if request.user.is_authenticated:
        token = request.user.token
        destination = "user:settings"
    if 'token' in request.session:
        token = Token.objects.get(value=request.session['token'])
        del request.session['token']
        destination = "user:index"
    if token != None:
        token.value = get_random_string(length=32)
        token.save()
        messages.success(request, "your token has been updated successfully")
    else: messages.warning(request, "your token does not load, try again later")
    return redirect(destination)