# Standard
import tempfile
from weasyprint import HTML, CSS
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.crypto import get_random_string
from django.contrib.auth import login as account_sign_in
from django.template.loader import render_to_string
from helpers.decorators import (
    resource, is_authenticated, is_guest, back
)
from helpers.functions import get_form_errors
from user.models import Token
from team.models import Membership
from .forms import KeyForm, PassWordResetForm


@is_authenticated(False)
@resource
def verify(request):
    if request.method == 'POST':
        form = KeyForm(request.POST)
        if form.is_valid():
            query = Token.objects.filter(key=form.cleaned_data['key'])
            if query.exists() and query.count() == 1:
                request.session['token'] = query.first().key
                messages.success(request, "your account has been verified successfully")
        else:
            get_form_errors(request, form)
    return redirect('home:retrieve_home_index')

@is_authenticated(False)
@resource
def signin(request):
    if request.method == 'POST':
        form = KeyForm(request.POST)
        if form.is_valid():            
            query = Token.objects.filter(key=form.cleaned_data['key'])
            if query.exists() and query.count() == 1:
                account_sign_in(request, query.first().user)
            messages.success(request, 'signed in successfully')
            return redirect("user:retrieve_account")
        else:
            get_form_errors(request, form)
    return redirect('home:retrieve_home_index')

@resource
def login(request):
    if request.method == 'POST':
        form = KeyForm(request.POST)
        if form.is_valid():
            query = Membership.objects.filter(key=form.cleaned_data['key'])
            if query.exists() and query.count() == 1:
                token = query.first()
                messages.success(request,"your membership has been verified successfully")
                request.session['space'] = token.space.id
                if not request.user.is_authenticated:
                    account_sign_in(request, token.user)
                return redirect("team:retrieve_team_index")
        else:
            get_form_errors(request, form)

@is_authenticated(True)
@is_guest(False)
def update_token(request):
    token = request.user.token
    if token != None:
        token.key = get_random_string(length=32)
        token.save()
        messages.success(request, "your token has been updated successfully")
    return redirect("user:retrieve_account")

@is_authenticated(False)
@back
def reset(request):
    if request.method == "POST":
        token = Token.objects.get(key=request.POST['key'])
        form = PassWordResetForm(token.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'password has been reset successfully')
            del request.session['token']
            return redirect("home:retrieve_home_index")
        else:
            get_form_errors(request, form)
            
def pdf(request):
    response                              = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition']       = f'inline; attachment; filename={request.user.username}.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    token  = Token.objects.get(user=request.user)
    html   = HTML(string=render_to_string('note/index.html',{'token':token, 'user':request.user}))
    css    = [CSS(f'/home/rhman/Documents/dj/scheme/user/static/user/css/pdf.css')]
    result = html.write_pdf(stylesheets=css)
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    return response