from django import forms
from .models import Signal, Note, Comment


class SignalForm(forms.ModelForm):

    message = forms.CharField(
        label=False,
        required=True,
        widget=forms.Textarea(
            attrs = {
                'data-field':"message",
                'autocomplete':"off",
                'maxlength':512,
            }
        )
    )

    class Meta:

        model   = Signal
        fields  = ['parent', 'message']
        widgets = {
            'parent': forms.HiddenInput(
                attrs = {
                    'data-field':"parent"
                }
            )
        }


class NoteForm(forms.ModelForm):

    message = forms.CharField(
        label=False,
        required=True,
        widget=forms.Textarea(
            attrs = {
                'placeholder':"Write your note",
                'data-field':"message",
                'autocomplete':"off",
                'maxlength':512,
            }
        )
    )

    class Meta:

        model = Note
        fields  = ['signal','message']
        widgets = {
            'signal': forms.HiddenInput(
                attrs = {
                    'data-field':"signal"
                }
            )
        }

class CommentForm(forms.ModelForm):

    message = forms.CharField(
        required=True,
        label=False
    )

    class Meta:

        model   = Comment
        fields  = ['parent', 'signal', 'message']
        widgets = {
            'parent': forms.HiddenInput(
                attrs={
                    'data-field':"parent",
                }
            ),
            'signal': forms.HiddenInput(
                attrs={
                    'data-field':"signal",
                }
            ),
            'message': forms.Textarea(
                attrs = {
                    'data-field':"message",
                    'autocomplete':"off",
                    'maxlength':512,
                }
            )
        }