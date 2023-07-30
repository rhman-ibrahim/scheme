import uuid

# Django
from django.contrib.auth import authenticate, login
from django.contrib.admin.models import CHANGE
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q

# Helpers
from helpers.functions import log

# Team
from team.models import Circle, CircleRequest

# User
from user.models import Account

def create_a_guest_user(request):
    uuid_key_8 = str(uuid.uuid4())[:8]
    uuid_key16 = str(uuid.uuid4())[:16]
    Account.objects.create_guest(
        username=uuid_key_8,
        password=uuid_key16
    )
    user = authenticate(
        username=uuid_key_8,
        password=uuid_key16
    )
    if user is not None:
        login(request, user)
        log(
            request.user.id,
            request.user,
            CHANGE,
            "signed in as a guest"
        )

def check_guest_activity(request):
    if request.user.is_guest:
        c = Circle.objects.filter(
            Q(founder=request.user) |
            Q(members=request.user)
        )
        r = CircleRequest.objects.filter(
            Q(user=request.user) &
            ~Q(status=0)
        )
        if c.exists() or r.exists():
            messages.info(request, "as a guest you can communicate only with 1 circle")
            return redirect("user:guest")
    pass
    