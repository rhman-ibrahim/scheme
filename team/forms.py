from django.core.exceptions import NON_FIELD_ERRORS
from django import forms
from .models import Space
from user.models import Account
from helpers.functions import (
    secret,
)

class SpaceForm(forms.ModelForm):

    founder = forms.IntegerField(
        required=True,
        widget=forms.HiddenInput()
    )
    name = forms.CharField(
        max_length=32,
        required=True,
        widget=forms.TextInput(
            attrs = {
                'placeholder':'name',
                'autocomplete':"off"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs = {
                'placeholder': "space password",
                'autocomplete':"new-password",
                'class':"password"
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

    def clean(self):
        if Space.objects.filter(name=self.cleaned_data['name'],founder__id=self.cleaned_data['founder']).exists():
            raise forms.ValidationError({'name': ['You have a circle with this name']})
        super().clean()

    def save(self):
        instance          = super().save(commit=False)
        instance.password = secret(self.cleaned_data['password'])
        instance.founder  = Account.objects.get(id=self.cleaned_data['founder'])
        instance.save()

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
                'autocomplete':'current-password',
                'class':"password"
            }
        )
    )

class AddFounderFriendsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs['instance']
        self.fields['members'].queryset = instance.founder_friends_queryset

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