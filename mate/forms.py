from django import forms


class RequestForm(forms.Form):

    identifier = forms.CharField(
        label='identifier',
        required=True,
        widget = forms.TextInput(
            attrs = {
                'id':'request-form-identifier',
                'autocomplete':'off'
            }
        )
    )
    message = forms.CharField(
        label="message",
        required=False,
        widget=forms.Textarea(
            attrs={
                'id':'request-form-message',
                'placeholder':'write a message (optional)',
                'autocomplete':'off',
                'maxlength':256
            }
        )
    )