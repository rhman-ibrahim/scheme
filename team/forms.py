from django import forms
from .models import Space


class SpaceForm(forms.ModelForm):

    name        = forms.CharField(
        max_length=32,
        required=True,
        widget=forms.TextInput(
            attrs = {
                'placeholder':'name',
                'autocomplete':"off"
            }
        )
    )
    password    = forms.CharField(
        widget=forms.PasswordInput(
            attrs = {
                'data-field':"password",
                'placeholder': "space password",
                'autocomplete':"new-password"
            }
        )
    )
    description = forms.CharField(
        max_length=512,
        required=False,
        widget=forms.Textarea(
            attrs = {
                'data-field':"description",
                'placeholder': "(optional)",
                'autocomplete':"off",
                'maxlength':512,
            }
        )
    )

    class Meta:
        model  = Space
        fields = ['name', 'password', 'description']


class SpaceLoginForm(forms.Form):

    name        = forms.CharField(
        max_length=32,
        required=True,
        widget=forms.TextInput(
            attrs={
                'autocomplete':'name',
            }
        )
    )
    password    = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete':'current-password'
            }
        )
    )

class AddFounderFriendsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs['instance']
        self.fields['members'].queryset = instance.founder_friends_queryset()

    class Meta:
        model   = Space
        fields  = ['members']
        widgets = {
            'members': forms.CheckboxSelectMultiple()
        }


class TransferSpaceForm(forms.ModelForm):

    members = forms.RadioSelect()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs['instance']
        self.fields['members'].queryset = instance.members.all()
    
    class Meta:
        model   = Space
        fields  = ['members']
        widgets = {
            'members': forms.RadioSelect()
        }