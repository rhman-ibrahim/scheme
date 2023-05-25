from django import forms
from .models import Circle, Invitation


class CircleForm(forms.ModelForm):

    name = forms.CharField(
        max_length=32,
        required=True
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
        fields = ['name', 'description']


class InvitationForm(forms.ModelForm):

    limit = forms.CharField(
        max_length=9,
        required=True
    )

    class Meta:
        model  = Invitation
        fields = ['limit']    
