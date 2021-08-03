from django.shortcuts import render
from .forms import CreateStoryForm,TechNewsForm
from django.http import HttpResponseRedirect
from .models import Stories,UserProfile,TechNews

# Create your views here.

def index(request):
    stories = Stories.objects.order_by("-id")
    technews = TechNews.objects.order_by("-id")
    context = {"stories":stories,
                "technews":technews}

    return render(request,"index.html",context)

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


def add_tech_news(request):
    form = TechNewsForm()
    if request.method == 'POST':
        form = TechNewsForm(request.POST or None,request.FILES)
        if form.is_valid():
            tech = form.save(commit=False)
            tech.creator = request.user
            tech.save()
        return HttpResponseRedirect(request.path_info)

    else:
        form = TechNewsForm()
    return render(request,"techform.html",{"form":form})

