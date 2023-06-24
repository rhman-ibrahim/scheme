import cv2
# Django
from django.contrib.auth import authenticate, login
from django.utils.crypto import get_random_string
from django.contrib.admin.models import CHANGE
from django.shortcuts import redirect
from django.contrib import messages
# Scheme
from scheme.settings import MEDIA_ROOT
# Helpers
from helpers.functions import get_form_errors, log
# User
from user.models import Token
from user.forms import  (
    SignUpForm, SignInForm, VerifyForm, PassWordResetForm
)
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
    return redirect('home:index')

@is_authenticated(False)
def reset(request):
    if 'token' in request.session and request.method == "POST":
        token = Token.objects.get(value=request.session['token'])
        form = PassWordResetForm(token.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'password has been reset successfully')
            del request.session['token']
            return redirect("home:index")
        else:
            get_form_errors(request, form)
    return redirect('user:back')