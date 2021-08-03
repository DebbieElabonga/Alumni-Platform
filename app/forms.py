from django import forms
from .models import Message

class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ['date_created']