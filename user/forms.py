from django import forms
from django.contrib.auth import authenticate
from django.core.validators import FileExtensionValidator
from django.contrib.auth.forms import (
    UserCreationForm, PasswordChangeForm, SetPasswordForm
)
from user.models import (
    Account, Token, Profile
)


class SignUpForm(UserCreationForm):

    username = forms.CharField(
        label='Username',
        help_text='usernames are 4 to 16 alphabetic/numeric characters.',
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
        help_text='at least 8 characters containing alphabetic/numeric characters and special characters.',
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
        help_text="repeat your password.",
        widget = forms.PasswordInput(
            attrs = {
                'id':'sign-up-form-password-2',
                'autocomplete':'new-password',
                'class':'password',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop("autofocus", None)

    class Meta:

        model  = Account
        fields = ['username']


class TokenForm(forms.ModelForm):
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
    class Meta:
        model  = Token
        fields = ['key']


class SignInForm(forms.ModelForm):

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
    
    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            try:
                account = Account.objects.get(username=username) 
            except Account.DoesNotExist:
                raise forms.ValidationError('account does not exist')
            if account.is_active == False:
                raise forms.ValidationError('your account has not been activated yet')
            if not authenticate(username=username, password=password):
                raise forms.ValidationError('password is incorrect')

    
    class Meta:

        model  = Account
        fields = ['username', 'password']

class PasswordUpdateForm(PasswordChangeForm):
    
    old_password = forms.CharField(
        label='Current',
        widget = forms.PasswordInput(
            attrs  = {
                'class':'password',
                'id':'password-update-form-old',
                'autocomplete':'current-password',
            }
        )
    )
    new_password1 = forms.CharField(
        label='New',
        widget = forms.PasswordInput(
            attrs  = {
                'class':'password',
                'id':'password-update-form-new',
                'autocomplete':'new-password',
            }
        )
    )
    new_password2 = forms.CharField(
        label='Confirm',
        widget = forms.PasswordInput(
            attrs = {
                'class':'password',
                'id':'password-update-form-confirm',
                'autocomplete':'new-password',
            }
        )
    )
    
    class Meta:

        model   = Account
        fields  = '__all__'

class PassWordResetForm(SetPasswordForm):
    
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
    
    class Meta:   
        model   = Account
        fields  = '__all__'


class AccountDeleteForm(forms.Form):

    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs  = {
                'class':'password',
                'id':'account-delete-password-form',
                'autocomplete':'current-password',
            }
        )
    )

class ProfileInfoForm(forms.ModelForm):
    
    name = forms.CharField(
        help_text="Separated names by spaces.",
        widget=forms.TextInput(
            attrs={
                'id':'profile-form-name',
                'autocomplete':'name',
            }
        )
    )
    email = forms.EmailField(
        help_text="Only you could see.",
        widget=forms.TextInput(
            attrs={
                'id':'profile-form-email',
                'autocomplete':'name',
            }
        )
    )
    about = forms.CharField(
        label="256",
        widget=forms.Textarea(
            attrs={
                'id':'profile-form-about',
                'autocomplete':'off',
                'maxlength':256
            }
        )
    )

    class Meta:
        model  = Profile
        fields = ['name', 'email', 'about']


class ProfilePictureForm(forms.ModelForm):
    
    picture = forms.ImageField(
        label="profile picture",
        help_text="supported formats are: JPEG and JPG.",
        validators = [
            FileExtensionValidator(allowed_extensions=['jpeg', 'jpg'])
        ]
    )

    class Meta:
        model  = Profile
        fields = ['picture']