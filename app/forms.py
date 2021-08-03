from .models import Idea
from django import forms
from .models import Stories,TechNews
from django.db.models import fields
from .models import Fundraiser, Message

class IdeaCreationForm(forms.ModelForm):
  class Meta:
    model = Idea
    fields = ('title', 'description','validity', 'image1_path', 'image2_path')
    widgets = {
      'title':forms.TextInput(attrs={'placeholder':'what idea do you need help...'}),
      'description':forms.Textarea(attrs={'placeholder':'Explain your idea to get more collaborators...'})
    }



class CreateStoryForm(forms.ModelForm):
    class Meta:
        model = Stories
        fields = ['title','description','image_path','link']



class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ['date_created']

class FundraiserForm(forms.ModelForm):
    class Meta:
        model = Fundraiser
        fields = ('__all__')
