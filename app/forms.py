from django.forms import widgets
from .models import Idea
from django import forms

class IdeaCreationForm(forms.ModelForm):
  model = Idea
  fields = ['title', 'description', 'image1_path', 'image2_path']
  widgets = {
    'title':forms.TextInput(attrs={'placeholder':'what idea do you need help...'}),
    'description':forms.Textarea(attrs={'placeholder':'Explain your idea to get more collaborators...'})
  }