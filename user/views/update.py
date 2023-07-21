# Django
from django.contrib.auth import update_session_auth_hash
from django.contrib.admin.models import CHANGE
from django.shortcuts import redirect
from django.contrib import messages
# Helpers
from helpers.functions import get_form_errors, log
from team.decorators import is_logined
# User
from user.models import Token
from user.decorators import is_authenticated, is_guest
from user.forms import PasswordUpdateForm, PassWordResetForm


@is_authenticated(True)
@is_guest(False)
@is_logined(False)
def update_password(request):
    if request.method == 'POST':
        form = PasswordUpdateForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            log(request.user.id, request.user, CHANGE, "updated password")
            messages.success(request, 'password has been updated successfully')
            return redirect("user:back")
        else:
            get_form_errors(request, form)
    return redirect('user:back')

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