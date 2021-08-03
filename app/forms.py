from django import forms
from .models import Stories,TechNews

class CreateStoryForm(forms.ModelForm):
    class Meta:
        model = Stories
        fields = ['title','description','image_path','link']

