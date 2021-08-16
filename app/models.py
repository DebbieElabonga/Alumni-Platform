from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields import TextField
from django.db.models.fields.files import ImageField
from tinymce import models as tiny_models
from django.db.models.signals import post_save
from django.dispatch import receiver
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
#Group/Cohort Model
class Group(models.Model):
  name = models.CharField(max_length=100)
  description = models.TextField()
  date_created = models.DateTimeField(auto_now_add=True)
  creator = models.ForeignKey(User, on_delete=CASCADE)
  admin = models.ForeignKey(User, related_name = 'admin', on_delete= CASCADE, null = True)
  is_private = models.BooleanField(default=False)
  class Meta:
    ordering = ['date_created']
  def __str__(self):
    return self.name
  @classmethod
  def get_groups(cls):
    return cls.objects.all()

#User profile model
class UserProfile(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="userprofile")
  bio = models.CharField(max_length=250)
  photo_path = models.ImageField(upload_to='Profiles/')
  group = models.ForeignKey(Group,related_name="group",on_delete=models.CASCADE,null=True)
  def __str__(self):
      return self.user.username
  def save_userprofile(self):
    self.save()
  @classmethod
  def get_users(cls):
    try:
      users = cls.objects.all()
    except cls.DoesNotExist:
      users = None
    return users
  #auto creates a user's profile once the user has registered
  @receiver(post_save, sender=User)
  def save_user(sender, instance, created, **kwargs):
    if created:
      UserProfile.objects.create(user=instance)

#General Admin Model
class GeneralAdmin(models.Model):
  profile = models.ForeignKey(UserProfile, on_delete = CASCADE)
  is_general_admin = models.BooleanField(default=True)
  def __str__(self):
      return self.profile.user.username
  @classmethod
  def get_admins(cls):
    try:
      admins = cls.objects.all()
    except cls.DoesNotExist:
      admins = None
    return admins
    
#Group/Cohort Model
#message/discussion Model
class Message(models.Model):
  title = models.CharField(max_length=100, blank=True, null=True)
  description = models.TextField()
  date_created = models.DateTimeField(auto_now_add=True)
  group = models.ForeignKey(Group, on_delete=CASCADE, null=True)
  creator = models.ForeignKey(User, on_delete=CASCADE)
  def __str__(self):
      return self.title
class Response(models.Model):
  message = models.ForeignKey(Message, on_delete = models.CASCADE)
  creator = models.ForeignKey(User, on_delete=CASCADE)
  reply = models.TextField()
  date_created = models.DateTimeField(auto_now_add=True)
  def __str__(self):
    return self.message
  def save_response(self):
    self.save()
  @classmethod
  def get_response(cls, message_id):
    return cls.objects.filter(message = message_id).all()
  @classmethod
  def get_groups(cls):
    try:
      groups = cls.objects.all()
    except cls.DoesNotExist:
      groups = None
    return groups
#StoryModel
class Stories(models.Model):
  title = models.CharField(max_length=100)
  description = tiny_models.HTMLField()
  image_path = models.ImageField(upload_to = 'Stories/')
  date_created = models.DateTimeField(auto_now_add=True)
  creator = models.ForeignKey(User, on_delete=CASCADE)
  link = models.CharField(max_length=250, null=True, blank=True)
  def __str__(self):
    return self.title
  @classmethod
  def get_stories(cls):
    try:
      stories = cls.objects.all()
    except cls.DoesNotExist:
      stories = None
    return stories
class Tech(models.Model):
  title = models.CharField(max_length=100)
  description = tiny_models.HTMLField()
  image_path = models.ImageField(upload_to = 'Stories/',null=True, blank=True)
  date_created = models.DateTimeField(auto_now_add=True)
  creator = models.ForeignKey(User, on_delete=CASCADE)
  link = models.CharField(max_length=250, null=True, blank=True)
  def __str__(self):
    return self.title
#Idea for finding collaborators, ie developers, Co-founders, mentors
class Idea(models.Model):
  title = models.CharField(max_length=200)
  description = tiny_models.HTMLField()
  image1_path = models.ImageField(upload_to = 'Ideas/')
  image2_path = models.ImageField(upload_to = 'Ideas/', blank = True, null = True)
  date_created = models.DateTimeField(auto_now_add=True)
  owner = models.ForeignKey(UserProfile, related_name='owner', on_delete=CASCADE)
  collaborators = models.ManyToManyField(UserProfile)
  interests = models.ManyToManyField(UserProfile, related_name='interests')
  validity = models.DateField()
  is_open = models.BooleanField(default=True)
  def __str__(self):
    return self.title
  @classmethod
  def get_open_projects(cls):
    try:
      projects = cls.objects.filter(is_open = True)
    except cls.DoesNotExist:
      projects = None
    return projects
  @classmethod
  def get_closed_projects(cls):
    try:
      projects = cls.objects.filter(is_open = False)
    except cls.DoesNotExist:
      projects = None
    return projects
#Fundraiser Model
class Fundraiser(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_path = models.ImageField(upload_to = 'Fundraisers/')
    creator = models.ForeignKey(UserProfile, on_delete=CASCADE)
    event_date = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
            return self.title
      
    @classmethod
    def getfundraisers(cls):
        try:
          all_fundraisers = cls.objects.all()
        except cls.DoesNotExist:
          all_fundraisers = None
        return all_fundraisers
    @property
    def lifespan(self):
      return '%s - present' % self.birthdate.strftime('%m/%d/%Y')
# Donor Model- No relation to Already existing users.
class Donor(models.Model):
  name = models.CharField(max_length=200)
  occupation = models.CharField(max_length=50 )
  is_alumni = models.BooleanField()
  pledge = models.TextField()
  fundaraiser = models.ForeignKey(Fundraiser, on_delete=CASCADE)
  date_created = models.DateTimeField(auto_now_add=True)
  def __str__(self):
    return self.title
#Invite user form model for storing uploaded csv
class UploadInvite(models.Model):
  file_path = models.FileField(upload_to='Files/')
  def __str__(self):
    return self.file_name

class Add_user(models.Model):
  full_name = models.CharField(max_length=200)
  username = models.CharField(max_length=20,default = 0)
  student_id = models.CharField(max_length = 10, unique=True)
  phone_number = models.CharField(max_length = 20, unique = True, default=None)
  email = models.CharField(max_length=100, default=None)
  def __str__(self):
    return self.full_name