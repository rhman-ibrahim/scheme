from django import forms
from .models import Room


class RoomForm(forms.Form):

    token = forms.CharField(
        label="room's token",
        widget = forms.HiddenInput(
            attrs = {
                'id':'user-token',
                'autocomplete':'off'
            }
        )
    )
    username = forms.CharField(
        label="room's username",
        widget = forms.HiddenInput(
            attrs = {
                'id':'user-username',
                'autocomplete':'off'
            }
        )
    )
    serial = forms.CharField(
        label="room's serial",
        widget = forms.HiddenInput(
            attrs = {
                'id':'room-serial',
                'autocomplete':'off'
            }
        )
    )
    message = forms.CharField(
        label=False,
        widget = forms.TextInput(
            attrs = {
                'id':'room-message',
                'placeholder':'message',
                'autocomplete':'off'
            }
        )
    )