from blog.models import Signal
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
        fields  = ['glyph', 'icon', 'parent', 'classification', 'body']
        widgets = {
            'glyph': forms.HiddenInput(
                attrs = {
                    'id':"signal-glyph-input",
                    'data-field':"glyph"
                }
            ),
            'icon': forms.HiddenInput(
                attrs = {
                    'id':"signal-icon-input",
                    'data-field':"icon"
                }
            ),
            'parent': forms.HiddenInput(
                attrs = {
                    'data-field':"parent"
                }
            ),
            'classification': forms.HiddenInput(
                attrs = {
                    'id':"signal-classification-input",
                    'data-field':"classification"
                }
            )
        }