# Django
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.contrib.admin.models import CHANGE
from django.shortcuts import redirect
from django.contrib import messages

# Helpers
from helpers.functions import get_form_errors, log
from team.decorators import is_logined

# User
from user.models import Token, Account
from user.decorators import is_authenticated, is_guest
from user.forms import (
    PasswordUpdateForm, PassWordResetForm, AccountDeleteForm
)


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

@is_authenticated(True)
@is_logined(False)
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
            return redirect("home:index")
        else:
            messages.error(request, "incorrect password")
    else:
        get_form_errors(request, form)
    return redirect('user:back')