from django.shortcuts import render
from .forms import CreateStoryForm
from django.http import HttpResponseRedirect
from .models import Stories,UserProfile,TechNews

# Create your views here.

def index(request):
    stories = Stories.objects.order_by("-id")
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
from .forms import DiscussionForm, FundraiserForm

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
