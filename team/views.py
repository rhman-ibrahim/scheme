# Django
from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from django.shortcuts import redirect, render
from django.contrib import messages

# Models
from ping.models import Room
from .models import Space

# Forms
from ping.forms import RoomForm
from .forms import (
    SpaceForm, SpaceLoginForm,
    AddFounderFriendsForm,
    TransferSpaceForm,
)

# Decorators
from helpers.decorators import (
    back, center, resource,
    is_authenticated,
    is_logined, is_founder
)

# Functions
from helpers.functions import (
    get_form_errors,
    create_a_guest_account,
    secret,
)

from django.contrib.auth import login as account_login


@back
def create_space(request):
    if not request.user.is_authenticated:
        create_a_guest_account(request)
    if request.method == "POST":
        form = SpaceForm(request.POST)
        if form.is_valid():
            if Space.objects.filter(name=form.cleaned_data['name'], founder=request.user).exists():
                messages.error(request, 'You have a space with this name.')
            else:
                space          = form.save(commit=False)
                space.founder  = request.user
                space.password = secret(form.cleaned_data['password'])
                space          = form.save()
                messages.success(request, "your space is created successfully")
        else:
            get_form_errors(request, form)


@is_authenticated(True)
@is_logined(True)
@resource
def retrieve_team_index(request):
    space = Space.objects.get(id=request.session.get('space'))
    room  = Room.objects.get(serial=space.serial)
    return render(
        request,
        "team/index.html",
        {
            'space': space,
            'room': room,
            'forms': {
                'team': {
                    'space': SpaceForm(instance=space),
                    'transfer':TransferSpaceForm(instance=space),
                },
                'mate': {
                    'friends': AddFounderFriendsForm(instance=space),
                },
                'ping': {
                    'room': RoomForm(initial={
                        'token': request.user.token.key,
                        'username': request.user.username,
                        'serial': room.serial
                    })
                }
            },
            'grid': {
                'title': f"{space.name} by {space.founder.username}",
                'icons': {
                    'left':"person",
                    'right':"menu",
                }
            }
        }    
    )

@is_authenticated(True)
@is_logined(True)
@is_founder
@back
def import_friends(request):
    if request.method == 'POST':
        space = Space.objects.get(id=request.session['space'])
        form = AddFounderFriendsForm(request.POST, instance=space)
        if form.is_valid():
            selected = [int(x) for x in request.POST.getlist('members')]
            if len(selected) > 0:
                space.members.add(*selected)
                messages.success(request, f"{len(selected)} friend/s added to your space.")
            messages.error(request, "You did not select any.")
        messages.error(request, "Something went wrong.")

@is_authenticated(True)
@is_logined(True)
@is_founder
@back
def remove_space_member(request, user_id):
    space = Space.objects.get(serial=request.session.get('space'))
    user   = space.members.get(id=int(user_id))
    space.members.remove(user)
    space.save()

@is_authenticated(True)
@is_logined(True)
@is_founder
@back
def transfer_space(request):
    space = Space.objects.get(id=request.session['space'])
    if request.method == 'POST':
        form = TransferSpaceForm(request.POST, instance=space)
        if form.is_valid():
            messages.info(request, form.cleaned_data['members'])

@is_authenticated(True)
@is_logined(False)
@back
def login(request):
    if request.method == 'POST':
        form = SpaceLoginForm(request.POST)
        if form.is_valid():
            space = Space.objects.get(name=form.cleaned_data['name'])
            if space.user_role(request.user) != None:       
                if space.check_password(form.cleaned_data['password']):
                    request.session['space'] = space.id
                    return redirect("team:retrieve_team_index")
                else:
                    messages.error(request, "space password is wrong")
            else:
                messages.warning(request, "you are not a member")
        else:
            get_form_errors(request, form)

@is_authenticated(True)
@is_logined(True)
@center
def logout(request):
    del request.session['space']

@is_authenticated(True)
@is_logined(True)
@center
def leave(request):
    space = Space.objects.get(id=request.session.get('space'))
    role   = space.user_role(request.user)
    if role == "member":
        space.members.remove(request.user)
        space.save()
    elif role == "founder":
        space.delete()
    return redirect('team:logout')