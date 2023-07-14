import cv2
# Django
from django.utils.crypto import get_random_string
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib import messages
# Scheme
from scheme.settings import MEDIA_ROOT
# Helpers
from helpers.functions import get_form_errors
# User
from user.models import Token
from user.forms import VerifyForm
from user.decorators import is_authenticated, is_guest


@is_authenticated(True)
@is_guest(False)
def token(request):
    with open(f"{MEDIA_ROOT}/user/tokens/{request.user.username}.png", 'rb') as f:
        file = f.read()
    response = HttpResponse(content_type='image/png')
    response.write(file)
    return response

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

@is_authenticated(True)
@is_guest(False)
def update_token(request):
    token = request.user.token
    if token != None:
        token.value = get_random_string(length=32)
        token.save()
        messages.success(request, "your token has been updated successfully")
    return redirect("user:settings")