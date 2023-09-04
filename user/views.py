import tempfile
from weasyprint import HTML, CSS
from django.template.loader import render_to_string
# Django
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import (
    update_session_auth_hash,
    logout,
)

# Models
from mate.models import Friendship
from .models import Account

# Forms
from mate.forms import SignalForm
from team.forms import SpaceForm, SpaceLoginForm
from ping.forms import RoomForm
from home.forms import KeyForm
from .forms import (
    PasswordUpdateForm, ProfileForm,
    PasswordConfirmForm
)

# Functions
from helpers.functions import get_form_errors
from helpers.decorators import back


def update_token(request):
    request.user.token.refresh()
    messages.success(request, "your token has been updated successfully")
    return redirect("user:account")

def update_password(request):
    if request.method == 'POST':
        form = PasswordUpdateForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'password has been updated successfully')
        else:
            get_form_errors(request, form)

def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form         = form.save(commit=False)
            form.account = request.user
            form.save()
            messages.success(request, "profile info updated successfully")
        else:
            get_form_errors(request, form)
            
def sign_out(request):
    if 'space' in request.session:
        request.session.pop('space')
    logout(request)
    messages.success(request, 'signed out successfully')
    return redirect('home:index')

def deactivate(request):
    request.user.deactivate()
    logout(request)
    messages.info(request, 'account has been deactivated')
    return redirect("home:index")

def pdf(request):
    if request.method == 'POST':
        form = PasswordConfirmForm(request.POST)
        if form.confirm():
            response                              = HttpResponse(content_type='application/pdf;')
            response['Content-Disposition']       = f'inline; attachment; filename={request.user.username}.pdf'
            response['Content-Transfer-Encoding'] = 'binary'
            html   = HTML(string=render_to_string('user/pdf.html',{'token':request.user.token, 'user':request.user}))
            css    = [CSS(f'/home/rhman/Documents/dj/scheme/user/static/user/css/pdf.css')]
            result = html.write_pdf(stylesheets=css)
            with tempfile.NamedTemporaryFile(delete=True) as output:
                output.write(result)
                output.flush()
                output = open(output.name, 'rb')
                response.write(output.read())
            return response
        else:
            get_form_errors(request, form)
            return redirect('user:account')

def friend(request, username):
    mate        = Account.objects.get(username=username)
    friendship  = Friendship.objects.filter(users__lte=2, users__in=[mate, request.user]).first()
    return render(
        request,
        "user/friend.html",
        {
            'grid': {
                'title':f'{ mate.username }',
                'icon':'menu'
            },
            'forms': {
                'ping': {
                    'room': RoomForm(
                        initial = {
                            'identifier': friendship.identifier,
                            'username': request.user.username,
                            'token': request.user.token.key
                        }
                    ),
                }
            },
            'mate':mate,
            'friendship':friendship,
            'room':friendship.room
        }
    )

def account(request):
    return render(
        request,
        "user/index.html",
        {
            'template': {
                'title': f'Settings / { request.user.username }',
                'icons': {
                    'left': 'layers',
                    'right': 'menu'
                },
                'forms': {
                    'password': PasswordUpdateForm(False),
                    'info': ProfileForm(instance=request.user.profile, auto_id="profile_info_%s"),
                    'friend_request':SignalForm(auto_id="friend_request_%s"),
                    'space_request':SignalForm(auto_id="space_request_%s"),
                    'login': SpaceLoginForm(auto_id="space_login_%s"),
                    'membership': KeyForm(auto_id="space_login_%s"),
                    'pdf': PasswordConfirmForm(
                        auto_id="account_pdf_%s",
                        initial={
                            'account':request.user.id
                        }
                    ),
                    'space': SpaceForm(
                        auto_id="space_%s",
                        initial={
                            'founder':request.user.id
                        }
                    ),
                }
            }
        }
    )