import datetime as dt
import mimetypes
import os
import random
import threading
from csv import DictReader
from email.message import EmailMessage

import stripe
from alumni.decorators import general_admin_required
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.base import File
from django.http import (HttpResponse, HttpResponseRedirect, JsonResponse,
                         request)
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View

from app.forms import (CohortForm, CreateStoryForm, DiscussionForm,
                       FundraiserForm, IdeaCreationForm, InviteUsers,
                       ResponseForm, SignupForm, TechNewsForm, UserProfileForm)
from app.models import (Fundraiser, GeneralAdmin, Group, Idea, Message,
                        Response, Stories, Tech, UploadInvite, User,
                        UserProfile)

from .email import collaborate_new, send_invite
from .forms import (Add_userForm, CohortForm, CreateStoryForm, DiscussionForm,
                    FundraiserForm, IdeaCreationForm, SignupForm, TechNewsForm,
                    UserProfileForm,UserCohortForm)
from .models import Group, Idea, Stories, Tech, UserProfile, Fundraiser
from .utils import generate_token


# Create your views here.
def index(request):
    groups = Group.objects.all()
    stories = Stories.objects.all().order_by("-id")
    tech = Tech.objects.all().order_by("-id")
    current_user = request.user

    #create story form
    if request.method == 'POST' and 'add_story' in request.POST:
        title = request.POST.get('story_title')
        desc = request.POST.get('description')
        image = request.FILES['image']
        date = dt.datetime.now()
        creator = request.user

        new_story = Stories(title = title, description = desc, image_path = image, date_created = date, creator = creator)
        new_story.save()

        context = {
        'logged_user':current_user,
        'groups':groups,'stories':stories,
        'tech':tech
        }
        return render(request,'index.html',context )
    
    if request.method == 'POST' and 'news_add' in request.POST:
        title = request.POST.get('news_title')
        desc = request.POST.get('description')
        image = request.FILES['image']
        date = dt.datetime.now()
        creator = request.user

        new_news = Tech(title = title, description = desc, image_path = image, date_created = date, creator = creator)
        new_news.save()

        context = {
        'logged_user':current_user,
        'groups':groups,
        'stories':stories,
        'tech':tech
        }
        return render(request,'index.html',context )

        

    context = {
        'logged_user':current_user,
        'groups':groups,'stories':stories,
        'tech':tech
        }
    return render(request,'index.html',context )

    
# def signup(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('index')
#     else:
#         form = SignupForm()
#     return render(request, 'registration/registration_form.html', {'form': form})


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
    title = "Cohorts"
    if request.method == 'POST':
        
        form = CohortForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user
            group.date_created = dt.datetime.now()
            group.save()
            group.creator.userprofile.group = group
            group.save()
            messages.success(request, 'A new Cohort has been created')
            return redirect('admin_dashboard')
        else:
            messages.warning(request, 'Invalid form')
            return render(request, 'cohort.html', {'title':title,'form': form})
    else:
        form = CohortForm()
    return render(request, 'cohort.html', {'title':title,'form': form})

def user_cohort(request):
    title = "Cohorts"
    if request.method == 'POST':
        
        form = UserCohortForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = request.user
            group.date_created = dt.datetime.now()
            group.save()
            group.creator.userprofile.group = group
            group.save()
            return redirect('index')
        else:
            return render(request, 'user_cohort.html', {'title':title,'form': form})
    else:
        form = UserCohortForm()
    return render(request, 'user_cohort.html', {'title':title,'form': form})

@login_required(login_url= 'login')  
def joincohort(request,id):
    current_user = request.user
    cohort = get_object_or_404(Group,pk=id)
    current_user.userprofile.group = cohort
    request.user.userprofile.save()
    print(current_user.userprofile.group)
    return redirect("cohortdiscussions",id)

@login_required(login_url= 'login')  
def leavecohort(request,id):
    current_user = request.user
    current_user.userprofile.group = None
    request.user.userprofile.save()

    return redirect("index")


#-----------------------------------------------------------------------------------------
#view function that renders to meet_collegues template
@login_required(login_url= 'login')  
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
        try:
            curr_user_prof = UserProfile.objects.filter(user = request.user).last()
        except UserProfile.DoesNotExist:
            curr_user_prof = None
        if curr_user_prof:
            new_idea.owner = UserProfile.objects.filter(user = request.user).last()
            new_idea.save()
            form = IdeaCreationForm
        else:
            messages.warning(request, 'You need to update your profile to proceed')
            return redirect('user_profile')


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
#-------------------------------------------------------------------------------------------------------------------
#   if idea.collaborators.userprofile.id == request.user.id:
#       messages.success(request, 'You are already a collaborator to this project')
#   else:  
#add a check if a user is already in the list of collaborators or interests then skip if so
#------------------------------------------------------------------------------------------------------------------------------------
    if request.method == 'POST':
        skills = request.POST.get('skills')
        new_join = request.user
        idea.interests.add(UserProfile.objects.filter(user = new_join).last())

        #send email of a user joining a team
        collaborate_new(new_join, idea, idea.owner.user.email, skills)
        messages.success(request, 'The owner has been Notified of your Interest. We will inform you once they accept your participation') 
        return redirect('meet_collegues')

    context = {
        'idea':idea
    }

    return render(request, 'singleidea.html', context)




@login_required(login_url= 'login')     
def create_story(request):
    form = CreateStoryForm()
    if request.method == 'POST':
        form = CreateStoryForm(request.POST or None,request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.creator = request.user
            story.save()
            return redirect('index')

    else:
        form = CreateStoryForm()
    return render(request,"storyform.html",{"form":form})


@login_required(login_url= 'login')  
def TechNews(request):
    form = TechNewsForm()
    if request.method == 'POST':
        form = TechNewsForm(request.POST or None,request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.creator = request.user
            news.save()
            return redirect('index')
    else:
        form = TechNewsForm()
    return render(request,'newsform.html',{"form":form})

# Create your views here.
@login_required(login_url= 'login')  
def Discussion(request, id):
# Start a discussion.

    current_user = request.user
    group = get_object_or_404(Group, pk=id)
    if request.method == 'POST':
        form = DiscussionForm(request.POST, request.FILES)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.creator = current_user
            discussion.group = group
            discussion.save()

        return redirect('cohortdiscussions',group.id)

    else:
        form = DiscussionForm()
    return render(request, 'new_discussion.html', {"form": form ,'group':group})
@login_required(login_url= 'login')  
def cohortdiscussions(request, id):
    group = get_object_or_404(Group, pk=id)
    messages = Message.objects.filter(group = group)
    members = UserProfile.objects.filter(group=group)

    return render(request, 'singlecohort.html', {'group':group , 'messages':messages,"members":members})
            
            
# stripe.api_key = settings.STRIPE_SECRET_KEY
# STRIPE_PUBLIC_KEY: settings.STRIPE_PUBLIC_KEY

          
""" ef donation(request):


    return render(request, 'singlecohort.html', {'group':group , 'messages':messages,"members":members}) """
    

def reply(request, id):
    user = request.user
    message = get_object_or_404(Message, pk=id)
    all_responses = Response.get_response(message.id)
    if request.method == 'POST':
        form = ResponseForm(request.POST, request.FILES)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.creator = user
            reply.message = message
            reply.save()

        return  HttpResponseRedirect(request.path_info)
        

    else:
        form = ResponseForm()
    return render(request, 'reply.html', {'all_responses':all_responses,"form": form, 'message':message})


    discussion.user = current_user
            
@login_required(login_url= 'login')        
@general_admin_required(login_url='user_profile', redirect_field_name='', message='You are not authorised to view this page.')            
def charge(request):
    
    if request.method == 'POST':
         print('Data:', request.POST)

    amount = int(request.POST['amount']) 

    customer = stripe.Customer.create(
            email=request.POST['email'],
            name=request.POST['nickname'],
            source=request.POST['stripeToken']
            )
    charge = stripe.Charge.create(
            customer=customer,
            amount=amount*100,
            currency='usd',
            description="Donation"
            )

    return redirect(reverse('success', args=[amount]))


def successMsg(request, args):
    amount = args
    return render(request, 'success.html', {'amount':amount})

    form = DiscussionForm()
    return render(request, 'new_discussion.html', {"form": form})

@login_required(login_url= 'login')  
@general_admin_required(login_url='user_profile', redirect_field_name='', message='You are not authorised to view this page.')  
def newfundraiser(request):
    title = 'Start A Fundraiser'
    current_user = request.user
    if request.method == 'POST':
        form = FundraiserForm(request.POST, request.FILES)
        if form.is_valid():
            fundraise = form.save(commit=False)
            fundraise.creator = UserProfile.objects.filter(user=current_user).last()
            fundraise.date_created = dt.datetime.now()
            fundraise.save()


    else:
        form = FundraiserForm()
    return render(request, 'new_fundraiser.html', {'title':title,"form": form})
#views to summary on the admin dashboard

@login_required(login_url= 'login')  
@general_admin_required(login_url='user_profile', redirect_field_name='', message='You are not authorised to view this page.')
def summary(request):
    '''
    renders summary on admin dashboard
    '''
    title = 'Admin - Summary'
    
    users = UserProfile.get_users()
    active_users = User.objects.filter(is_active = True)
    inactive_users = User.objects.filter(is_active = False)

    projects = Idea.get_open_projects()
    closed_projects = Idea.get_closed_projects()
    groups = Group.get_groups()
    admins = GeneralAdmin.get_admins()[:5]
    articles = Stories.get_stories()


    def close_project():
        project_id = request.POST.get('close_proj')
        project = Idea.objects.filter(id = project_id)
        if project:
            project.update(is_open = False)
    
    if request.method == 'POST':
        close_project()

        return redirect('admin_dashboard')


    context = {
        'inactive_users':inactive_users,
        'closed_projects':closed_projects,
        'articles':articles,
        'admins':admins,
        'users':users,
        'projects':projects,
        'groups':groups,
        'title':title
    }

    return render(request, 'admin_dash/dashboard.html', context)

#view function that renders to invite members page

@login_required(login_url= 'login')  
@general_admin_required(login_url='user_profile', redirect_field_name='', message='You are not authorised to view this page.')
def invite_members(request):
    '''
    renders invite member form
    invites single users
    invotes multiple users
    '''
    def invite_new_user(f_name, l_name, email):

        rando = random.randint(0, 1000)
        new_user = User(username = f_name+l_name+str(rando), first_name = f_name, last_name = l_name, email = email, is_active = False)
        new_user.save()
        current_site = get_current_site(request)
        domain = current_site.domain
        uid = urlsafe_base64_encode(force_bytes(new_user.pk))
        token = generate_token.make_token(new_user)
        
        send_invite(email, domain , uid, token)

        messages.success(request,'Congratulations! You have succesfully Invited New users!')
        return redirect('invite_members')
    title = 'Invite Members'
    if 'single_invite' in request.POST and request.method == "POST":
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        email = request.POST.get('user_email')

        #call the function that sends email to new users
        invite_new_user(f_name, l_name, email)
    form = InviteUsers

    if 'multiple_invite' in request.POST and request.method == 'POST':
        form = InviteUsers(request.POST, request.FILES)
        if form.is_valid:
            form.save()

            form_to_read = UploadInvite.objects.all().last()

            with open((form_to_read.file_path).path, 'r') as read_obj:
                csv_dict_reader = DictReader(read_obj)
                for row in csv_dict_reader:
                    f_name = row['first_name']
                    l_name = row['last_name']
                    email = row['email']

                    invite_new_user(f_name, l_name, email)
       
    context = {
        'form':form,
        'title':title,
    }

    return render(request, 'invite_member.html', context)

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
            messages.add_message(request, messages.SUCCESS, 'Welcome! You are now an active User.')
            warning = 'You will not be able to edit this information when this window is closed or refreshed.'
            context = {
                'edit_warning':warning,
                'user':user
            }
            messages.success(request, '<h4>Edit or Confirm your details below </h4>')           
            return render(request, 'edit_details.html', context)
        is_expired = True

        context = {
            'is_expired':is_expired
        }  

        messages.warning(request, 'Invitation Link has Expired!')
        return render(request, 'edit_details.html', context)
#--------------------------------------------------------------------------------------------
#function enabling dowloading of user csv file
def download_csv(request):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = 'Invite_users.csv'

    filepath = BASE_DIR + '/app/Files/' + filename
    path = open(filepath, 'r')
    mime_type = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type = mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename

    return response

    
    return render(request, 'admin_dash/dashboard.html', context)

# view function that edits a users details when they accept initation.
def edit_details(request):
    '''
    renders to edit page
    '''
    form_password = SignupForm
    if request.method == 'POST' and 'save_default_details' in request.POST:
        user_id = request.POST.get('user_id')
        username = request.POST.get("username")
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        password = request.POST.get('password')
        bio = request.POST.get('bio')
        photo_path = request.FILES['photo']

        user_to_update = User.objects.filter(id = user_id)
        user_to_update.update(username = username, first_name = f_name, last_name = l_name)
        curr_user = User.objects.get(id = user_id)
        curr_user.set_password(password)
        curr_user.save()
        user_profile = UserProfile.objects.filter(user = user_id)

        if user_profile:
            user_profile.update(bio = bio, photo_path = photo_path)
        else:
            new_profile = UserProfile(user = user_to_update, bio = bio, photo_path = photo_path)
            new_profile.save()
        
        to_login = authenticate(request, username = username, password = password)
        if to_login is not None:
            login(request, to_login)
        else:
            messages.warning('User details not Found')
            redirect('login')
        messages.success(request, 'Your Account has been Updated successfully')
        return redirect('user_profile')
    else:
        direct_access = True
        context = {
            'form_password':form_password,
            'direct_access':direct_access
        }  
        messages.warning(request, 'This Page can only be accessed through a valid invite link')
        return render(request, 'edit_details.html', context)


# def create_user(request):
#     '''
#     View function to add a new students members into the alumni platform and send them an invitation email
#     '''
#     if request.method == 'POST':
#         form = Add_userForm(request.POST)
#         email = request.POST.get('email')
#         if form.is_valid():
#             user = form.save(commit = False)
#             user.is_active = False
#             user.save()
#             current_site = get_current_site(request)
#             email_subject = 'Invitation to Alumni Community'
#             message = render_to_string('invitation.html',
#                                     {
#                                         'user': user,
#                                         'domain': current_site.domain,
#                                         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                                         'token': generate_token.make_token(user)
#                                     }
#                                     )
#             email_message = EmailMessage(
#                 email_subject,
#                 message,
#                 settings.EMAIL_HOST_USER,
#                 [email]
#             )
#             EmailThread(email_message).start()
#             messages.add_message(request, messages.SUCCESS,
#                                 'invaitation sent  succesfully')
#             return redirect('registration')

#             messages.success(request, f'Congratulations! You have succesfully Added a new User!')
#             return redirect('/user_list/')
#     else:
#         form = Add_userForm()
#     return render(request, 'create_user.html', {"form": form})


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
            messages.add_message(request, messages.SUCCESS, 'user is invited successfully')

            return redirect('')
        return render(request, '')

class EmailThread(threading.Thread):

    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()

def project_fundraisers(request):
    all_fundraisers=Fundraiser.getfundraisers()
    context = {
        'all_fundraisers': all_fundraisers
        }

    return render(request, 'fundraisers.html',context) 
def single_fundraiser(request, id):
    fundraiser = Fundraiser.objects.get(id=id)
    return render(request, 'single_fundraiser.html', {'fundraiser':fundraiser})



  
  
