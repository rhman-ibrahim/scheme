from signals.models import LearningThread, TestingThread
from django import forms


class LearningThreadForm(forms.ModelForm):

    signal = forms.CharField(
        label=False,
        required=True,
        widget=forms.Textarea(
            attrs = {
                'data-field':"signal",
                'autocomplete':"off",
                'maxlength':512,
            }
        )
    )

    class Meta:

        model = LearningThread
        fields  = ['parent','signal']
        widgets = {
            'signal': forms.HiddenInput(
                attrs = {
                    'data-field':"parent"
                }
            )
        }


class TestingThreadForm(forms.ModelForm):

    signal = forms.CharField(
        label=False,
        required=True,
        widget=forms.Textarea(
            attrs = {
                'data-field':"signal",
                'autocomplete':"off",
                'maxlength':512,
            }
        )
    )

    class Meta:

        model   = TestingThread
        fields  = ['parent', 'signal']
        widgets = {
            'parent':
            forms.HiddenInput(
                attrs={
                    'data-field':"parent",
                }
            )
        }