from app.forms import IdeaCreationForm
from django.shortcuts import render

# Create your views here.

#-----------------------------------------------------------------------------------------
#view function that renders to meet_collegues template
def meet_collegues(request):
  '''
  renders meet_collegues template
  '''
  form = IdeaCreationForm
  if request.method == 'POST':
    


  context = {
    'form':form

  }
  return render(request, 'meetcollegues.html', context)