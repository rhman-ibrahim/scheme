from blog.models import Post
from django import forms


class PostForm(forms.ModelForm):

    signal = forms.RadioSelect()
    body   = forms.CharField(
        label     = False,
        required  = True,
        widget=forms.Textarea(
            attrs = {
                'data-field':"body",
                'autocomplete':"off",
                'maxlength':512,
            }
        )
    )

    class Meta:

        model   = Post
        fields  = ['parent', 'signal', 'body']
        widgets = {
            'parent': forms.HiddenInput(
                attrs = {
                    'id':"signal-parent-input",
                    'data-field':"parent"
                }
            ),
            'signal': forms.RadioSelect()
        }