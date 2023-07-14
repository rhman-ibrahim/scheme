from django import forms
from django.core.validators import FileExtensionValidator
from user.models import Account
from .models import Profile

class ProfileInfoForm(forms.ModelForm):
    
    name = forms.CharField(
        help_text="Separated names by spaces.",
        widget=forms.TextInput(
            attrs={
                'id':'profile-form-name'
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


class AccountUsernameForm(forms.Form):

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