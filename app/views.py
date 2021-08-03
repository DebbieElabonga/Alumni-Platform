from django.shortcuts import render

# Create your views here.

#-----------------------------------------------------------------------------------------
#view function that renders to meet_collegues template
def meet_collegues(request):
  '''
  renders meet_collegues template
  '''

  context = {

  }
  return render(request, 'meetcollegues.html', context)