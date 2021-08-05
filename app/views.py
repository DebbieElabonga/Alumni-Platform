import datetime as dt

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Idea, Stories,UserProfile,TechNews,Group
from .forms import SignupForm,UserProfileForm,CohortForm,TechNewsForm,IdeaCreationForm,DiscussionForm,FundraiserForm,CreateStoryForm
from django.shortcuts import redirect,render

# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):
    groups = Group.objects.all()

    return render(request,'index.html', {'groups':groups})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'registration/registration_form.html', {'form': form})

@login_required(login_url='/accounts/login/')    
def profile(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if  profile_form.is_valid():
            profile_form.save()
            return redirect('index')
    else:
        profile_form = UserProfileForm(instance=request.user)
    return render(request, 'user_profile.html',{ "profile_form": profile_form})

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

# @login_required(login_url='/accounts/login/')
# def join_cohort(request, id):
#     group = get_object_or_404(Group, id=id)
#     request.user.group = group
#     request.user.save()
#     return redirect('index')

# @login_required(login_url='/accounts/login/')
# def leave_cohort(request, id):
#     group = get_object_or_404(Group, id=id)
#     request.user.group = None
#     request.user.save()
#     messages.success(
#         request, 'Success! You have succesfully exited this Cohort ')
#     return redirect('index')

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


# Create your views here.

def index(request):
    stories = Stories.objects.order_by("-id")
    technews = TechNews.objects.order_by("-id")
    return render(request,"index.html",{"stories":stories,"technews":technews})
    
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
            discussion.creator = current_user
            discussion.date_created = dt.datetime.now()

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
            fundraise.creator = current_user
            fundraise.date_created = dt.datetime.now()
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
