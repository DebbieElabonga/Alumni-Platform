from .models import Cohort
from django import forms

class ChatForm(forms.ModelForm):
    class Meta:
        model = Cohort
        fields = ('name', 'description', 'members', 'is_private', 'discussion' )
       