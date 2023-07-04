# Django
from django.contrib.auth import update_session_auth_hash
from django.contrib.admin.models import CHANGE
from django.shortcuts import redirect
from django.contrib import messages
# Helpers
from helpers.functions import get_form_errors, log
# User
from user.decorators import is_authenticated, is_guest
from user.forms import PasswordUpdateForm


@is_authenticated(True)
@is_guest(False)
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