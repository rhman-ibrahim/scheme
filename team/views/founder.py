# Django
from django.shortcuts import redirect
from django.contrib.admin.models import CHANGE
from django.contrib import messages

# Models
from team.models import Circle, CircleRequest
from team.forms import AddFounderFriendsForm, TransferCircleForm

# Functions & Decorators
from team.decorators import is_logined
from user.decorators import is_authenticated
from user.functions import log


@is_authenticated(True)
@is_logined(True)
def put(request):
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
    return redirect("user:back")

@is_authenticated(True)
@is_logined(True)
def transfer(request):
    circle = Circle.objects.get(id=request.session['circle'])
    if request.method == 'POST':
        form = TransferCircleForm(request.POST, instance=circle)
        if form.is_valid():
            messages.info(request, form.cleaned_data['members'])
    return redirect("user:back")

@is_authenticated(True)
@is_logined(True)
def approve(request, user_id):
    c_req        = CircleRequest.objects.get(circle__serial=request.session.get('circle'), user__id=user_id)
    c_req.status = 1
    c_req.circle.members.add(c_req.user)
    c_req.circle.save()
    c_req.save()
    log(
        request.user.id, c_req.circle, CHANGE,
        f"approved ({c_req.user.username}) joining the circle ({c_req.circle.name})."
    )
    return redirect("team:browse")
    
@is_authenticated(True)
@is_logined(True)
def reject(request, user_id):
    c_req        = CircleRequest.objects.get(circle__serial=request.session.get('circle'), user__id=user_id)
    c_req.status = 0
    c_req.circle.save()
    c_req.save()
    log(
        request.user.id, c_req.circle, CHANGE,
        f"rejected ({c_req.user.username}) joining the circle ({c_req.circle.name})."
    )
    return redirect("team:browse")

@is_authenticated(True)
@is_logined(True)
def remove(request, user_id):
    circle = Circle.objects.get(serial=request.session.get('circle'))
    user   = circle.members.get(id=int(user_id))
    circle.members.remove(user)
    circle.save()
    log(
        request.user.id, circle, CHANGE,
        f"removed ({user.username}) from the circle ({circle.name})."
    )
    return redirect("team:browse")