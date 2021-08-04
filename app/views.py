from app.models import Group, UserProfile
from app.forms import CohortForm, SignupForm, UserProfileForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime as dt

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

@login_required(login_url='/accounts/login/')
def join_cohort(request, id):
    group = get_object_or_404(Group, id=id)
    request.owner.profile.group = group
    request.owner.profile.save()
    return redirect('index')

@login_required(login_url='/accounts/login/')
def leave_cohort(request, id):
    group = get_object_or_404(Group, id=id)
    request.owner.profile.group = None
    request.owner.profile.save()
    messages.success(
        request, 'Success! You have succesfully exited this Cohort ')
    return redirect('index')
