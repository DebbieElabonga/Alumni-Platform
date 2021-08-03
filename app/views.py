from django.shortcuts import render,redirect
from .forms import DiscussionForm

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