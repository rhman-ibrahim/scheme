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
                'autocomplete':"off",
                'placeholder':"token's key"
            }
        )
    )
    new_password1 = forms.CharField(
        label = 'Password',
        widget = forms.PasswordInput(
            attrs = {
                'autocomplete':'new-password',
                'id':'reset-form-new-password-1',
                'placeholder':'new password',
                'class':'password',
            }
        )
    )
    new_password2 = forms.CharField(
        label = 'Confirm',
        widget = forms.PasswordInput(
            attrs = {
                'autocomplete':'new-password',
                'id':'reset-form-new-password-2',
                'placeholder':'confirm password',
                'class':'password',
            }
        )
    )