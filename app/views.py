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


