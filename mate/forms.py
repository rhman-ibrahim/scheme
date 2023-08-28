from django import forms


class SignalForm(forms.Form):

    identifier = forms.CharField(
        label='identifier',
        required=True,
        widget = forms.TextInput(
            attrs = {
                'autocomplete':'off'
            }
        )
    )
    message = forms.CharField(
        label="message",
        required=False,
        widget=forms.Textarea(
            attrs={
                'placeholder':'write a message (optional)',
                'autocomplete':'off',
                'maxlength':256
            }
        )
    )