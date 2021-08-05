from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields import TextField
from django.db.models.fields.files import ImageField
from tinymce import models as tiny_models

# Create your models here.
# Using django base user
#-------------------------------------------------------------------------------------------
#username
#first_name
#last_name
#email
#password1
#password2

#-----------------------------------------------------------------------
#User profile model
class UserProfile(models.Model):
  user = models.ForeignKey(User, on_delete=CASCADE)
  bio = models.CharField(max_length=250)
  photo_path = models.ImageField(upload_to='Profiles/')

  def __str__(self):
      return self.user.username

#General Admin Model
class GeneralAdmin(models.Model):
  profile = models.ForeignKey(UserProfile, on_delete = CASCADE)
  is_general_admin = models.BooleanField(default=True)

  def __str__(self):
      return self.profile.user.username

#message/discussion Model
class Message(models.Model):
  title = models.CharField(max_length=100, blank=True, null=True)
  description = models,TextField()
  date_created = models.DateTimeField()

  def __str__(self):
      return self.title

#Group/Cohort Model
class Cohort(models.Model):
  name = models.CharField(max_length=100)
  description = models.TextField()
  date_created = models.DateTimeField()
  creator = models.ForeignKey(User, on_delete=CASCADE)
  admin = models.ForeignKey(UserProfile, related_name = 'admin', on_delete= CASCADE)
  members = models.ManyToManyField(UserProfile)
  is_private = models.BooleanField(default=False)
  discussion = models.ForeignKey(Message, on_delete=CASCADE, null=True)
  class Meta:
    ordering = ['date_created']

  def __str__(self):
    return self.name

#Story/News Model
class Stories(models.Model):
  title = models.CharField(max_length=100)
  description = tiny_models.HTMLField()
  image_path = models.ImageField(upload_to = 'Stories/')
  date_created = models.DateTimeField()
  creator = models.ForeignKey(UserProfile, on_delete=CASCADE)
  link = models.CharField(max_length=250, null=True, blank=True)

  def __str__(self):
    return self.title

#Idea for finding collaborators, ie developers, Co-founders, mentors
class Idea(models.Model):
  title = models.CharField(max_length=200)
  description = tiny_models.HTMLField()
  image1_path = models.ImageField(upload_to = 'Ideas/')
  image2_path = models,ImageField(upload_to = 'Ideas/', blank = True, null = True)
  date_created = models.DateTimeField()
  owner = models.ForeignKey(UserProfile, related_name='owner', on_delete=CASCADE)
  collaborators = models.ManyToManyField(UserProfile)
  validity = models.DateTimeField()
  is_open = models.BooleanField(default=True)

  def __str__(self):
    return self.title

#Fundaraiser Model
class Fundraiser(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField()
  image_path = models.ImageField(upload_to = 'Fundraisers/')
  creator = models.ForeignKey(UserProfile, on_delete=CASCADE)
  event_date = models.DateField()
  date_created = models.DateTimeField()

  def __str__(self):
    return self.title

# Donor Model- No relation to Already existing users.
class Donor(models.Model):
  name = models.CharField(max_length=200)
  occupation = models.CharField(max_length=50 )
  is_alumni = models.BooleanField()
  pledge = models.TextField()
  fundaraiser = models.ForeignKey(Fundraiser, on_delete=CASCADE)
  date_created = models.DateTimeField()

  def __str__(self):
    return self.title

