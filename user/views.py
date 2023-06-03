import cv2

# Django
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.utils.crypto import get_random_string
from django.shortcuts import render, redirect

# Scheme
from scheme.settings import MEDIA_ROOT

# Helpers
from helpers.functions import get_form_errors, log

# Circles
from circles.forms import CircleForm
from circles.models import Circle

# User
from .models import Token
from .forms import  (
    SignUpForm, SignInForm, VerifyForm, ProfilePictureForm,
    PasswordUpdateForm, ProfileInfoForm, PassWordResetForm
)
from .functions import create_a_guest_user
from .decorators import authentication


def guest(request):

    if not request.user.is_authenticated:
        create_a_guest_user(request)

    return render(
        request,
        "user/guest.html",
        {
            'forms': {
                'circle': CircleForm
            }
        }
    )

@authentication(True)
def settings(request):
    return render(
        request,
        "user/settings.html",
        {
            'forms': {
                'info': ProfileInfoForm(instance=request.user.profile),
                'password': PasswordUpdateForm(False),
                'picture': ProfilePictureForm,
                'circle': CircleForm
            }
        }
    )

@authentication(True)
def token(request):
    with open(f"{MEDIA_ROOT}/user/tokens/{request.user.username}.png", 'rb') as f:
        file = f.read()
    response = HttpResponse(content_type='image/png')
    response.write(file)
    return response

def identified(request):
    token = Token.objects.get(value=request.session['token'])
    if 'token' in request.session:
        return render(
            request,
            "user/identified.html",
            {
                'user': token.user,
                'forms': {
                    'reset': PassWordResetForm(token.user),
                }
            }
        )
    return redirect('home:user')

@authentication(False)
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, "your account has been created successfully.")
        else:
            get_form_errors(request, form)
        return redirect("home:user")
    
@authentication(False)
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
                return redirect("user:settings")
        else:
            get_form_errors(request, form)
    return redirect("home:user")

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
    return redirect('user:identified')

def reset(request):
    if 'token' in request.session and request.method == "POST":
        token = Token.objects.get(value=request.session['token'])
        form = PassWordResetForm(token.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'password has been reset successfully')
            del request.session['token']
            return redirect("home:user")
        else:
            get_form_errors(request, form)
    return redirect('home:user')

@authentication(True)
def update_token(request):
    token = request.user.token
    if token != None:
        token.value = get_random_string(length=32)
        token.save()
        messages.success(request, "your token has been updated successfully")
    return redirect("user:settings")

@authentication(True)
def update_profile_picture(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form         = form.save(commit=False)
            form.account = request.user
            form.save()
            log(request.user.id, request.user, CHANGE, "updated profile picture")
            messages.success(request, "profile picture updated successfully")
        else:
            get_form_errors(request, form)
    return redirect('home:user')

@authentication(True)
def update_password(request):
    if request.method == 'POST':
        form = PasswordUpdateForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            log(request.user.id, request.user, CHANGE, "updated password")
            messages.success(request, 'password has been updated successfully')
            return redirect("home:user")
        else:
            get_form_errors(request, form)
    return redirect('home:user')

@authentication(True)
def update_profile_info(request):
    if request.method == 'POST':
        form = ProfileInfoForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form         = form.save(commit=False)
            form.account = request.user
            form.save()
            log(request.user.id, request.user, CHANGE, "updated profile info")
            messages.success(request, "profile info updated successfully")
        else:
            get_form_errors(request, form)
    return redirect('user:settings')

@authentication(True)
def signout(request):
    log(request.user.id, request.user, CHANGE, "signed out")
    logout(request)
    messages.success(request, 'signed out successfully')
    return redirect('home:user')

def cancel(request):
    if 'token' in request.session: del request.session['token']
    return redirect("home:index")

def navigate(request):
    if request.user.is_authenticated:
        if request.user.is_guest:
            return redirect("user:guest")
        return redirect("user:settings")
    return redirect("home:user")