# Django
from django.shortcuts import redirect
from django.contrib import messages

# Helpers
from helpers.functions import get_form_errors
from helpers.decorators import is_logged

# Team
from team.models import Space, Membership
from team.forms import SpaceLoginForm


def log_in(request):
    if request.method == 'POST':
        form = SpaceLoginForm(request.POST)
        if form.is_valid():
            space = Space.objects.get(name=form.cleaned_data['name'])
            if Membership.objects.filter(space=space, user=request.user).exists():       
                if space.check_password(form.cleaned_data['password']):
                    request.session['space'] = space.id
                    return redirect("team:index")
                else:
                    messages.error(request, "space password is wrong")
            else:
                messages.warning(request, "you are not a member")
        else:
            get_form_errors(request, form)


@is_logged(True)
def refresh(request, id):
    membership = Membership.objects.get(id=id)
    membership.refresh()

@is_logged(True)
def log_out(request):
    del request.session['space']

@is_logged(True)    
def leave(request):
    space = Space.objects.get(id=request.session.get('space'))
    space.members.remove(request.user)
    return redirect('team:logout')