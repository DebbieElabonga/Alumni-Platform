from django import forms
from django.db.models import fields
from .models import Fundraiser, Message

class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ['date_created']

class FundraiserForm(forms.ModelForm):
    class Meta:
        model = Fundraiser
        fields = ('__all__')