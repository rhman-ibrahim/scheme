from signals.models import Signal
from django import forms


class SignalForm(forms.ModelForm):

    body = forms.CharField(
        label=False,
        required=True,
        widget=forms.Textarea(
            attrs = {
                'data-field':"body",
                'autocomplete':"off",
                'maxlength':512,
            }
        )
    )

    class Meta:

        model   = Signal
        fields  = ['parent', 'body']
        widgets = {
            'parent': forms.HiddenInput(
                attrs = {
                    'data-field':"parent"
                }
            )
        }