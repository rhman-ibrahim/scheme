from django.shortcuts import render, redirect

from user.functions import create_a_guest_user
from user.decorators import authenticated

from helpers.decorators import resource

from .models import Invitation

@authenticated(True)
def form(request):
    return render(request, "circles/form.html")

@authenticated(True)
def manage(request):
    return render(request, "circles/manage.html")

def index(request):
    return render(request, "circles/index.html")

@resource("circles:connect")
def invitation(request, uuid):
    inv = Invitation.objects.get(uuid=uuid)
    if not request.user.is_authenticated:
        create_a_guest_user(request)
    inv.invitees.add(request.user)
    inv.circle.members.add(request.user)
    inv.save()
    inv.circle.save()
    return redirect("circles:connect")