# Django
from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from django.shortcuts import redirect, render
from django.contrib import messages
from django.db.models import Q

# Models
from team.models import (
    Circle, CircleRequest
)
from ping.models import Room
# from blog.models import Post

# Forms
# from blog.forms import PostForm
from team.forms import (
    CircleForm, CircleRequestForm,
    AddFounderFriendsForm, TransferCircleForm,
    CircleLoginForm
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
        form  = CircleRequestForm(request.POST)
        if form.is_valid():
            circle          = Circle.objects.get(serial=form.cleaned_data['serial'])
            circle_request  = CircleRequest.objects.get(circle=circle, user=request.user)
            if circle_request.status == 2:
                messages.info(request, f"Your request to join {circle.name} is pending")
            elif circle_request.status == 1:
                messages.info(request, f"You are already connected to {circle.name}")
            else:
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
        else:
            get_form_errors(request, form)


@is_authenticated(True)
@is_logined(True)
@resource
def retrieve_team_index(request):
    circle = Circle.objects.get(id=request.session.get('circle'))
    room   = Room.objects.get(serial=circle.serial)
    return render(
        request,
        "team/index.html",
        {
            'circle': circle,
            'room': room,
            'forms': {
                'circle': CircleForm(instance=circle),
                'friends': AddFounderFriendsForm(instance=circle),
                'transfer':TransferCircleForm(instance=circle),
            },
            'grid': {
                'title': f".sch | {circle.name}",
                'icons': {
                    'left':"groups",
                    'right':"forum",
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
@is_founder
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
@is_founder
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
@is_founder
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
@is_founder
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
            circle = Circle.objects.get(name=form.cleaned_data['name'])
            if circle.user_role(request.user) != None:       
                if circle.check_password(form.cleaned_data['password']):
                    request.session['circle'] = circle.id
                    return redirect("team:retrieve_team_index")
                else:
                    messages.error(request, "circle password is wrong")
            else:
                messages.warning(request, "you are not a member")
        else:
            get_form_errors(request, form)

@is_authenticated(True)
@is_logined(True)
@center
def logout(request):
    del request.session['circle']

@is_authenticated(True)
@is_logined(True)
@center
def leave(request):
    circle = Circle.objects.get(id=request.session.get('circle'))
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
    return redirect('team:logout')

@is_authenticated(True)
@is_logined(True)
@back
def delete_request(request, request_id):
    circle_request = CircleRequest.objects.get(id=request_id)
    if request.user == circle_request.user:
        circle_request.delete()
        log(
            request.user.id, circle_request.circle, DELETION,
            f"approved ({circle_request.user.username}) joining the circle ({circle_request.circle.name})."
        )
        messages.warning(
            request,
            "You are not allowed to preform this action"
        )
        return redirect("team:retrieve_team_index")