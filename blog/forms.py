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
        fields  = ['parent', 'glyph', 'icon', 'classification', 'body']
        widgets = {
            'parent': forms.HiddenInput(
                attrs = {
                    'id':"signal-parent-input",
                    'data-field':"parent"
                }
            ),
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
            'classification': forms.HiddenInput(
                attrs = {
                    'id':"signal-classification-input",
                    'data-field':"classification"
                }
            )
        }