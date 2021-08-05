from app.models import Cohort, Message, UserProfile
from app.forms import ChatForm
from django.shortcuts import render, redirect

# Create your views here.
def chat(request):
    current_user = request.user
    if request.method == 'POST':
        form = ChatForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False) 
            post.user = current_user

            post.save()

        return redirect('group')

    else:
        form = ChatForm()

    return render(request, 'chat.html', {'form':form})

def group(request):
    groups = Cohort.objects.all()
    groups = groups[::-1]
    params = {
        'groups': groups,
    }
    return render(request, 'group.html', params)
