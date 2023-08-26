from django import forms
from django.contrib.auth.forms import SetPasswordForm


class KeyForm(forms.Form):
    
    key        = forms.CharField(
        label    = "key",
        required = True,
        widget=forms.TextInput(
            attrs = {
                'placeholder':"your key",
                'autocomplete':"off"
            }
        )
    )

class PassWordResetForm(SetPasswordForm):
    
    key        = forms.CharField(
        label="token",
        required=True,
        widget=forms.TextInput(
            attrs = {
                'placeholder':"token's key",
                'autocomplete':"off"
            }
        )
    )
    new_password1 = forms.CharField(
        label = 'Password',
        widget = forms.PasswordInput(
            attrs = {
                'class':'password',
                'id':'reset-form-new-password-1',
                'autocomplete':'new-password',
            }
        )
    )
    new_password2 = forms.CharField(
        label = 'Confirm',
        widget = forms.PasswordInput(
            attrs = {
                'class':'password',
                'id':'reset-form-new-password-2',
                'autocomplete':'new-password',
            }
        )
    )