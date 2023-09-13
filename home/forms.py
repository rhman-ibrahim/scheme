from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, SetPasswordForm,
    AuthenticationForm
)
from user.models import Account

class SignUpForm(UserCreationForm):

    username = forms.CharField(
        label='Username',
        widget = forms.TextInput(
            attrs = {
                'id':'sign-up-form-username',
                'pattern':'^[a-zA-Z0-9]{4,16}$',
                'autocomplete':'username'
            }
        )
    )
    password1 = forms.CharField(
        label='Password',
        widget = forms.PasswordInput(
            attrs = {
                'id':'sign-up-form-password-1',
                'autocomplete':'new-password',
                'class':'password',
            }
        )
    )
    password2 = forms.CharField(
        label='Confirm',
        widget = forms.PasswordInput(
            attrs = {
                'id':'sign-up-form-password-2',
                'autocomplete':'new-password',
                'class':'password',
            }
        )
    )

    class Meta:

        model  = Account
        fields = ['username', 'password1', 'password2']


class SignInForm(AuthenticationForm):

    username = forms.CharField(
        label='Username',
        widget = forms.TextInput(
            attrs = {
                'id':'sign-in-form-username',
                'pattern':'^[a-zA-Z0-9]{4,16}$',
                'autocomplete':'username',
            }
        )
    )
    password = forms.CharField(
        label='Password',
        widget = forms.PasswordInput(
            attrs = {
                'id':'sign-in-form-password',
                'autocomplete':'current-password',
                'class':'password',
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