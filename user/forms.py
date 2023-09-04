from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password
from user.models import Account, Profile

class PasswordConfirmForm(forms.Form):

    account  = forms.IntegerField(
        widget=forms.HiddenInput(

        )
    )
    
    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs  = {
                'class':'password',
                'id':'password-confirm-form',
                'autocomplete':'current-password',
            }
        )
    )

    def confirm(self):
        if self.is_valid():
            account = Account.objects.get(id=self.cleaned_data['account'])
            if check_password(self.cleaned_data['password'], account.password):
                return True
            else:
                self.add_error('password', 'wrong password')



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


class ProfileForm(forms.ModelForm):
    
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
        label="about",
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