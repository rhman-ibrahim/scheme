from blog.models import Post, Comment
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

class CommentForm(forms.ModelForm):

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

        model   = Comment
        fields  = ['parent', 'signal', 'post', 'body']
        widgets = {
            'parent': forms.HiddenInput(
                attrs = {
                    'id':"signal-parent-input",
                    'data-field':"parent"
                }
            ),
            'post': forms.HiddenInput(
                attrs = {
                    'id':"signal-post-input",
                    'data-field':"post"
                }
            ),
            'signal': forms.RadioSelect()
        }