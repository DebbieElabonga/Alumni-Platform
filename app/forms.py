from django import forms
from .models import Stories,TechNews

class CreateStoryForm(forms.ModelForm):
    class Meta:
        model = Stories
        fields = ['title','description','image_path','link']

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
