from .models import Idea
from django import forms

class IdeaCreationForm(forms.ModelForm):
  class Meta:
    model = Idea
    fields = ('title', 'description','validity', 'image1_path', 'image2_path')
    widgets = {
      'title':forms.TextInput(attrs={'placeholder':'what idea do you need help...'}),
      'description':forms.Textarea(attrs={'placeholder':'Explain your idea to get more collaborators...'})
    }