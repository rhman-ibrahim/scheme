from django.contrib import messages
from django.shortcuts import render, redirect

from helpers.decorators import resource
from helpers.functions import get_form_errors

from user.functions import create_a_guest_user
from user.decorators import authenticated

from .models import Circle, Invitation
from .forms import CircleForm


def create(request):

    if  request.method == "POST":
        form = CircleForm(request.POST)
        
        if not request.user.is_authenticated:
            create_a_guest_user(request)

        if form.is_valid():
            circle         = form.save(commit=False)
            circle.founder = request.user
            form.save()
            request.session['circle'] = f'{circle.id}'
            messages.success(request, "your circle is created successfully")
        else:
            get_form_errors(request, form)

    return redirect("circles:manage")


@authenticated(True)
def manage(request):
    circle = Circle.objects.get(id=request.session.get('circle'))
    return render(
        request,
        "circles/manage.html",
        {
            'circle': circle,
            'forms': {
                'circle': CircleForm(instance=circle)
            }
        }
    )

def index(request):
    return render(
        request,
        "circles/index.html",
        {
            'forms': {
                'circle': CircleForm
            }
        }
    )

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