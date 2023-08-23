from django import forms


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