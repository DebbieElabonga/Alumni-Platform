from django.conf import settings
from django.contrib.auth.models import User
from django.views.generic.base import View
from app.models import Group, UserProfile, Stories,Idea,Tech
from app.forms import CohortForm, SignupForm, UserProfileForm,IdeaCreationForm,CreateStoryForm,TechNewsForm
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime as dt
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.utils.encoding import force_text
import threading
from threading import Thread
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from app.utils import generate_token

# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):
    groups = Group.objects.all()
    stories = Stories.objects.order_by("-id")
    tech = Tech.objects.all()
    return render(request,'index.html', {'groups':groups,'stories':stories,'tech':tech})
    
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'registration/registration_form.html', {'form': form})

   
def profile(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if  profile_form.is_valid():
            profile_form.save()
            return redirect('index')
    else:
        profile_form = UserProfileForm(instance=request.user)
        context = { 
            "profile_form": profile_form
            }
    return render(request, 'user_profile.html',context)

def cohort(request):
    if request.method == 'POST':
        form = CohortForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user
            group.date_created = dt.datetime.now()
            group.save()
            group.members.add(UserProfile.objects.get(user=request.user))
            group.members.add(request.POST.get('admin'))
            group.save()
            messages.success(request, 'A new Cohort has been created')
            return redirect('index')
        else:
            messages.warning(request, 'Invalid form')
            return render(request, 'cohort.html', {'form': form})
    else:
        form = CohortForm()
    return render(request, 'cohort.html', {'form': form})

# Create your views here.

#-----------------------------------------------------------------------------------------
#view function that renders to meet_collegues template
def meet_collegues(request):
  '''
  renders meet_collegues template
  '''
  form = IdeaCreationForm
  try:
    ideas = Idea.objects.all()
  except Idea.DoesNotExist:
    ideas = None
  if request.method == 'POST':
    form = IdeaCreationForm(request.POST, request.FILES)
    if form.is_valid():
      new_idea = form.save(commit=False)
      new_idea.date_created = dt.datetime.now()
      new_idea.owner = UserProfile.objects.get(id = 1)#change filter to user = request.user
      new_idea.save()

      try:
        ideas = Idea.objects.all()
      except Idea.DoesNotExist:
        ideas = None

      context = {
        'form':form,
        'ideas':ideas
        }
      return render(request, 'meetcollegues.html', context)

    else:
      messages.warning(request, 'Invalid Form')
      return redirect('meet_collegues')

  context = {
    'form':form,
    'ideas':ideas

  }
  return render(request, 'meetcollegues.html', context)

#view function that renders to single idea page
def single_idea(request, id):
  '''
  Renders a found idea object
  '''
  idea = Idea.objects.get(id = id)
  if request.method == 'POST':
    skills = request.POST.get('skills')
    new_join = request.user
    idea.collaborators.add(1) #use user profile query UserProfile.objects.filter(user = new_join).last()
    #send email of a user joining a team
    
  context = {
    'idea':idea
  }

  return render(request, 'singleidea.html', context)
  return render(request, 'meetcollegues.html', context)



def index(request):
    stories = Stories.objects.order_by("-id")
    # technews = TechNews.objects.order_by("-id")
    return render(request,"index.html",{"stories":stories})
    
def create_story(request):
    form = CreateStoryForm()
    if request.method == 'POST':
        form = CreateStoryForm(request.POST or None,request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.creator = request.user
            story.save()
        return HttpResponseRedirect(request.path_info)

    else:
        form = CreateStoryForm()
    return render(request,"storyform.html",{"form":form})


from django.shortcuts import render,redirect
from .forms import Add_userForm, DiscussionForm, FundraiserForm, TechNewsForm

def TechNews(request):
    form = TechNewsForm()
    if request.method == 'POST':
        form = TechNewsForm(request.POST or None,request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.creator = request.user
            news.save()
        return HttpResponseRedirect(request.path_info)
    else:
        form = TechNewsForm()
    return render(request,'newsform.html',{"form":form})

# Create your views here.
def Discussion(request):
    current_user = request.user
    if request.method == 'POST':
        form = DiscussionForm(request.POST, request.FILES)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.user = current_user

            discussion.save()

        return redirect('index')

    else:
        form = DiscussionForm()
    return render(request, 'new_discussion.html', {"form": form})
    
def Fundraiser(request):
    current_user = request.user
    if request.method == 'POST':
        form = FundraiserForm(request.POST, request.FILES)
        if form.is_valid():
            fundraise = form.save(commit=False)
            fundraise.user = current_user

            fundraise.save()

        return redirect('index')

    else:
        form = FundraiserForm()
    return render(request, 'new_fundraiser.html', {"form": form})
#views to summary on the admin dashboard
def summary(request):
  '''
  renders summary on admin dashboard
  '''
  title = 'admin dashboard summary'

  context = {
    'title':title
  }

  return render(request, 'admin_dash/dashboard.html', context)

def create_user(request):
    '''
    View function to add a new students members into the alumni platform and send them an invitation email
    '''
    if request.method == 'POST':
        form = Add_userForm(request.POST)
        email = request.POST.get('email')
        if form.is_valid():
            user = form.save(commit = False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Invitation to Alumni Community'
            message = render_to_string('invitation.html',
                                    {
                                        'user': user,
                                        'domain': current_site.domain,
                                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                        'token': generate_token.make_token(user)
                                    }
                                    )
            email_message = EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [email]
            )
            EmailThread(email_message).start()
            messages.add_message(request, messages.SUCCESS,
                                'invaitation sent  succesfully')
            return redirect('registration')

            messages.success(request, f'Congratulations! You have succesfully Added a new User!')
            return redirect('/user_list/')
    else:
        form = Add_userForm()
    return render(request, 'create_user.html', {"form": form})


class InviteUserView(View):
    '''
    View function that generates a new token for each new user based on their uid
    '''
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None
        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.add_message(request, messages.SUCCESS,
                                 'user is invited successfully')
            return redirect('')
        return render(request, '')

class EmailThread(threading.Thread):

    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()