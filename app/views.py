from app.forms import CohortForm, SignupForm, UserProfileForm
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):

    return render(request,'index.html')

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
            cohort = form.save(commit=False)
            cohort.user = request.user
            cohort.save()
            messages.success(request, 'A new Cohort has been created')
            return redirect('index')
    else:
        form = CohortForm()
    return render(request, 'cohort.html', {'form': form})