# Django
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from django.contrib import messages
from django.http import Http404
from django.db.models import Q

# Models
from team.models import (
    Circle, CircleRequest
)
from ping.models import Room
from blog.models import Post

# Forms
from blog.forms import PostForm
from team.forms import (
    CircleForm, CircleRequestForm,
    AddFounderFriendsForm, TransferCircleForm,
    CircleLoginForm
)
# Decorators
from helpers.decorators import back, home
from user.decorators import is_authenticated
from team.decorators import is_logined

# Functions
from helpers.functions import (
    get_form_errors,
    secret,
    log,
)

@back
def create_circle(request):
    if request.method == "POST":
        form = CircleForm(request.POST)
        if form.is_valid():
            if Circle.objects.filter(name=form.cleaned_data['name'], founder=request.user).exists():
                messages.error(request, 'You have a circle with this name.')
            else:
                circle          = form.save(commit=False)
                circle.founder  = request.user
                circle.password = secret(form.cleaned_data['password'])
                circle          = form.save()
                log(
                    request.user.id, circle, ADDITION,
                    f"created the circle ({circle.name})."
                )
                messages.success(request, "your circle is created successfully")
        else:
            get_form_errors(request, form)

@back
def create_request(request):
    if request.method == 'POST':
        try:
            form  = CircleRequestForm(request.POST)
            if form.is_valid():
                # 1: check
                circle = get_object_or_404(Circle, serial=form.cleaned_data['serial'])
                query  = CircleRequest.objects.filter(circle=circle, user=request.user)
                # 2: if the request is there and not rejected (status != 0)
                if query.exists() and query.first().status != 0:
                    if query.first().status == 2:
                        messages.info(request, f"Your request to join {query.first().circle.name} is pending")
                    elif query.first().status == 1:
                        messages.info(request, f"You are already connected to {query.first().circle.name}")
                else:
                    # 3: if request is not there or it is there and rejected
                    CircleRequest.objects.create(
                        circle=circle,
                        user=request.user
                    )
                    messages.success(
                        request,
                        "join request created successfully."
                        )
                    log(
                        request.user.id, circle, ADDITION,
                        f"requested to join the circle ({circle.name})."
                    )
            else: get_form_errors(request, form)
        except Http404:
            messages.error(request, "circle does not exists")


@is_authenticated(True)
@is_logined(True)
def retrieve_team_settings(request):
    circle = Circle.objects.get(id=request.session.get('circle'))
    return render(
        request,
        "team/settings.html",
        {
            'circle': circle,
            'forms': {
                'circle': CircleForm(instance=circle),
                'friends': AddFounderFriendsForm(instance=circle),
                'transfer':TransferCircleForm(instance=circle),
            },
            'column': {
                'icon':"groups"
            }
        }    
    )

@is_authenticated(True)
@is_logined(True)
def retrieve_team_index(request):
    circle = Circle.objects.get(id=request.session.get('circle'))
    request.session['parent_signal_id'] = None
    return render(
        request,
        "team/index.html",
        {
            'circle': circle,
            'room': Room.objects.get(serial=circle.serial),
            'posts': Post.objects.filter(circle=circle, level=0).order_by('-created'),
            'forms': {
                'post': PostForm
            },
            'column': {
                'left':"menu",
                'right':"forum",
            }
        }    
    )

@is_authenticated(True)
@is_logined(True)
@back
def import_friends(request):
    if request.method == 'POST':
        circle = Circle.objects.get(id=request.session['circle'])
        form = AddFounderFriendsForm(request.POST, instance=circle)
        if form.is_valid():
            selected = [int(x) for x in request.POST.getlist('members')]
            if len(selected) > 0:
                circle.members.add(*selected)
                messages.success(request, f"{len(selected)} friend/s added to your circle.")
            messages.error(request, "You did not select any.")
        messages.error(request, "Something went wrong.")

@is_authenticated(True)
@is_logined(True)
@back
def accept_request(request, user_id):
    c_req        = CircleRequest.objects.get(circle__id=request.session.get('circle'), user__id=user_id)
    c_req.status = 1
    c_req.circle.members.add(c_req.user)
    c_req.circle.save()
    c_req.save()
    log(
        request.user.id, c_req.circle, CHANGE,
        f"approved ({c_req.user.username}) joining the circle ({c_req.circle.name})."
    )
    
@is_authenticated(True)
@is_logined(True)
@back
def reject_request(request, user_id):
    c_req        = CircleRequest.objects.get(circle__serial=request.session.get('circle'), user__id=user_id)
    c_req.status = 0
    c_req.circle.save()
    c_req.save()
    log(
        request.user.id, c_req.circle, CHANGE,
        f"rejected ({c_req.user.username}) joining the circle ({c_req.circle.name})."
    )

@is_authenticated(True)
@is_logined(True)
@back
def remove_circle_member(request, user_id):
    circle = Circle.objects.get(serial=request.session.get('circle'))
    user   = circle.members.get(id=int(user_id))
    circle.members.remove(user)
    circle.save()
    log(
        request.user.id, circle, CHANGE,
        f"removed ({user.username}) from the circle ({circle.name})."
    )

@is_authenticated(True)
@is_logined(True)
@back
def transfer_circle(request):
    circle = Circle.objects.get(id=request.session['circle'])
    if request.method == 'POST':
        form = TransferCircleForm(request.POST, instance=circle)
        if form.is_valid():
            messages.info(request, form.cleaned_data['members'])

@is_authenticated(True)
@is_logined(False)
@back
def login(request):
    if request.method == 'POST':
        form = CircleLoginForm(request.POST)
        if form.is_valid():
            query = Circle.objects.filter(
                Q(name=form.cleaned_data['name']) &
                (Q(founder=request.user) | Q(members=request.user))
            )
            circle = query.first() if query.exists() else None
            if circle.check_password(form.cleaned_data['password']):
                request.session['circle'] = circle.id
                return redirect("team:retrieve_team_index")
            else:
                messages.error(request, "circle password is wrong")
        else:
            get_form_errors(request, form)

@is_authenticated(True)
@is_logined(True)
@home
def logout(request):
    del request.session['circle']

@is_authenticated(True)
@is_logined(True)
@home
def leave(request):
    circle = Circle.objects.get(serial=request.session.get('circle'))
    role   = circle.user_role(request.user)
    if role == "member":
        circle.members.remove(request.user)
        log(request.user.id, circle, CHANGE,
            f"left the circle ({circle.name})."
        )
        circle.save()
    elif role == "founder":
        circle.delete()
        log(request.user.id, circle, DELETION,
            f"deleted the circle ({circle.name})."
        )

@is_authenticated(True)
@is_logined(True)
def delete_request(request, request_id):
    c_req        = CircleRequest.objects.get(id=request_id)
    c_req.delete()
    log(
        request.user.id, c_req.circle, DELETION,
        f"approved ({c_req.user.username}) joining the circle ({c_req.circle.name})."
    )
    return redirect("team:retrieve_team_index")