from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# The signup form
class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=300, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
