from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from django.contrib import messages
from helpers.decorators import resource
from helpers.functions import get_form_errors, log
from user.functions import create_a_guest_user
from user.decorators import authentication
from .models import Circle, Invitation
from .forms import CircleForm, InvitationForm


def create(request):
    if  request.method == "POST":
        form = CircleForm(request.POST)
        if not request.user.is_authenticated:
            create_a_guest_user(request)
        if form.is_valid():
            circle         = form.save(commit=False)
            circle.founder = request.user
            circle         = form.save()
            log(
                request.user.id,
                circle,
                ADDITION,
                f"created the circle"
            )
            request.session['circle'] = f'{circle.id}'
            messages.success(request, "your circle is created successfully")
        else:
            get_form_errors(request, form)
    return redirect("circles:manage")

def invite(request):
    if  request.method == "POST":
        circle      = Circle.objects.get(id=request.session.get('circle'))
        form        = InvitationForm(request.POST)
        if form.is_valid():
            invitation         = form.save(commit=False)
            invitation.circle  = circle
            invitation         = form.save()
            log(
                request.user.id,
                circle,
                ADDITION,
                f"created an invitation for {invitation.limit} memebers"
            )
        else:
            get_form_errors(request, form)
    return redirect("circles:manage")

@authentication(True)
def manage(request):
    circle      = Circle.objects.get(id=request.session.get('circle'))
    return render(
        request,
        "circles/manage.html",
        {
            'circle': circle,
            'logs': LogEntry.objects.filter(
                content_type = ContentType.objects.get_for_model(Circle),
                object_id    = circle.id
            ),
            'invitations': Invitation.objects.filter(circle=circle),
            'states': {
                'description': True if circle.description else False,
                'founder':True if circle.founder == request.user else False
            },
            'forms': {
                'circle': CircleForm(instance=circle),
                'invitation': InvitationForm
            }
        }
    )

@resource("home:circles")
def invitation(request, uuid):
    inv = Invitation.objects.get(uuid=uuid)
    if not request.user.is_authenticated:
        create_a_guest_user(request)
    inv.invitees.add(request.user)
    inv.circle.members.add(request.user)
    inv.save()
    inv.circle.save()
    return redirect("circles:connect")

def terminate(request):
    if request.session['circle']: del request.session['circle']
    return redirect("user:navigate")