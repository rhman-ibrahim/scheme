from django import forms
from .models import Room


class RoomForm(forms.ModelForm):

    name = forms.CharField(
        label='room name',
        widget = forms.TextInput(
            attrs = {
                'id':'room-name',
                'placeholder':'room name'
            }
        )
    )

    class Meta:
        model   = Room
        fields  = ['name', 'users', 'description']
        widgets = {
            'users': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(
                attrs={
                    'placeholder':'What is this room for?'
                }
            )
        }