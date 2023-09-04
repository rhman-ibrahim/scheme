# Django
from django.shortcuts import render

# Models
from team.models import Space, Membership

# Forms
from ping.forms import RoomForm
from team.forms import (
    SpaceForm, AddFounderFriendsForm,
    TransferSpaceForm,
)
from mate.forms import SignalForm
from user.forms import PasswordConfirmForm

# Decorators
from helpers.decorators import (
    is_logged, is_founder
)


@is_logged(True)
def index(request):
    space = Space.objects.get(id=request.session.get('space'))
    return render(
        request,
        "team/index.html",
        {
            'template': {
                'icon':'menu',
                'title':f"{space.name} by {space.founder.username}",
                'instances': {
                    'membership': Membership.objects.get(user=request.user, space=space),
                    'space': space,
                },
                'forms': {
                    'room': RoomForm(
                        initial = {
                            'identifier': space.identifier,
                            'username': request.user.username,
                            'token': request.user.token.key
                        }
                    )
                }
            }
        }    
    )

@is_founder
def founder(request):
    space      = Space.objects.get(id=request.session.get('space'))
    return render(
        request,
        "team/founder.html",
        {   
            'template': {
                'title': f"{space.name} Settings",
                'instances': {
                    'space': space
                },
                'forms': {
                    'invitation': SignalForm(auto_id="space_invitation_%s"),
                    'delete': PasswordConfirmForm(auto_id="space_delete_%s"),
                    'leave': PasswordConfirmForm(auto_id="space_leave_%s"),
                    'import': AddFounderFriendsForm(instance=space),
                    'transfer': TransferSpaceForm(instance=space),
                    'space': SpaceForm(instance=space)
                }
            }
        }    
    )

@is_logged(True)
def member(request, id):
    membership = Membership.objects.get(id=id)
    return render(
        request,
        "team/membership.html",
        {
            'template': {
                'title': f'{membership.space.name} / {membership.user.username}',
                'instances': {
                    'membership': membership,
                },
                'forms': {
                    'team': {
                        'terminate': PasswordConfirmForm(auto_id="space_leave_%s")
                    },
                }
            }
        }
    )