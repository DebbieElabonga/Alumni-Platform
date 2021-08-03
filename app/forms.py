from django import forms
from .models import Message

class PostForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ['date_created']