from app.models import UserProfile
from app.forms import IdeaCreationForm
from django.shortcuts import redirect, render
from django.contrib import messages
import datetime as dt

# Create your views here.

#-----------------------------------------------------------------------------------------
#view function that renders to meet_collegues template
def meet_collegues(request):
  '''
  renders meet_collegues template
  '''
  form = IdeaCreationForm
  if request.method == 'POST':
    form = IdeaCreationForm(request.POST, request.FILES)
    if form.is_valid():
      new_idea = form.save(commit=False)
      new_idea.date_created = dt.datetime.now()
      new_idea.owner = UserProfile.objects.get(id = 1)#change filter to user = request.user
      new_idea.save()

      context = {
        'form':form
        }
      return render(request, 'meetcollegues.html', context)

    else:
      messages.warning(request, 'Invalid Form')
      return redirect('meet_collegues')

  context = {
    'form':form

  }
  return render(request, 'meetcollegues.html', context)