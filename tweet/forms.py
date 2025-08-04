from django import forms
from .models import Tweet , Comment

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['image', 'content']



class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-sm',
        'placeholder': 'Write a comment...'
    }), max_length=500)

    class Meta:
        model  = Comment
        fields = ['content']
