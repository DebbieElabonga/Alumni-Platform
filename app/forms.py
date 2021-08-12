from app.models import Group, UserProfile, Message, Response
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Idea
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets
from .models import Idea, UploadInvite, Stories,Tech, Fundraiser, Message, Group, UserProfile
from .models import Add_user, Idea
from .models import Stories,Tech
from .models import Idea
from .models import Fundraiser, Message
from bootstrap_datepicker_plus import DatePickerInput

#edit details form 

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')
        

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user', 'photo_path', 'bio']

class CohortForm(forms.ModelForm):
    class Meta:
        model = Group 
        fields = [ 'name','description','is_private','admin']


class IdeaCreationForm(forms.ModelForm):
  class Meta:
    model = Idea
    fields = ('title', 'description','validity', 'image1_path', 'image2_path')
    widgets = {
      'validity':(DatePickerInput(attrs={'placeholder':'YYYY/MM/DD'})),
      'title':forms.TextInput(attrs={'placeholder':'what idea do you need help...'}),
      'description':forms.Textarea(attrs={'placeholder':'Explain your idea to get more collaborators...'})
    }



class CreateStoryForm(forms.ModelForm):
    class Meta:
        model = Stories
        fields = ['title','description','image_path','link']


class TechNewsForm(forms.ModelForm):
    class Meta:
        model = Tech
        fields = ['title','description','image_path','link']


class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ['date_created', 'group', 'creator']

class FundraiserForm(forms.ModelForm):
    class Meta:
        model = Fundraiser
        fields = ('__all__')

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['reply']
class Add_userForm(forms.ModelForm):
    class Meta:
        model = Add_user
        fields = ('full_name','student_id','phone_number','email')

        widgets = {
            'full_name': forms.TextInput(attrs={'class':'form-conrtol'}),
            'id_number': forms.TextInput(attrs={'class':'form-conrtol'}),
            'phone_number': forms.TextInput(attrs={'class':'form-conrtol'}),
            'email': forms.TextInput(attrs={'class':'form-conrtol'}),
        }
        exclude = ['date_created']

class InviteUsers(forms.ModelForm):
    class Meta:
        model = UploadInvite
        fields = ['file_path']
