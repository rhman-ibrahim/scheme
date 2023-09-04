# Django
from django.shortcuts import redirect
from django.contrib import messages

# Models
from team.models import Space, Membership

# Forms
from team.forms import (
    SpaceForm, TransferSpaceForm,
    AddFounderFriendsForm
)

# Functions
from helpers.decorators import (
    is_founder, back
)
from helpers.functions import (
    get_form_errors,
    create_a_temporary_account
)

@back
def instance(request):
    if not request.user.is_authenticated:
        create_a_temporary_account(request)
    if request.method == "POST":
        form = SpaceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "your space is created successfully"
            )
        else:
            get_form_errors(request, form)


@is_founder
def friends(request):
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

@is_founder
def transfer(request):
    space = Space.objects.get(id=request.session['space'])
    if request.method == 'POST':
        form = TransferSpaceForm(request.POST, instance=space)
        if form.is_valid():
            messages.info(request, form.cleaned_data)

@is_founder
def terminate(request, id):
    membership = Membership.objects.get(id=id)
    membership.remove()

@is_founder
def delete(request, id):
    pass