from django import forms 
from .models import Tweet

class TweetForm(forms.ModelForm):
    body = forms.CharField(required=True,widget=forms.widgets.Textarea(attrs={'placeholder':'Enter your tweet','class':'form-control'}), label="")
    class Meta:
        model = Tweet
        exclude = ['user']