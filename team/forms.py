from django import forms
from django.core.exceptions import ValidationError
from .models import Circle


class CircleForm(forms.ModelForm):

    name        = forms.CharField(
        max_length=32,
        required=True
    )
    password    = forms.CharField(
        widget=forms.PasswordInput()
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
        model  = Circle
        fields = ['name', 'password', 'description']


class CircleLoginForm(forms.Form):

    name        = forms.CharField(
        max_length=32,
        required=True,
    )
    password    = forms.CharField(
        required=True,
        widget=forms.PasswordInput()
    )