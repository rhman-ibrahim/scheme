# Django
from django.contrib.auth import update_session_auth_hash
from django.contrib.admin.models import CHANGE
from django.shortcuts import redirect
from django.contrib import messages
# Helpers
from helpers.functions import get_form_errors, log
# User
from user.decorators import is_authenticated, is_guest
from user.forms import  (
    ProfilePictureForm, PasswordUpdateForm, ProfileInfoForm
)


@is_authenticated(True)
@is_guest(False)
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
    return redirect('user:back')

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

@is_authenticated(True)
@is_guest(False)
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