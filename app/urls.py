from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from app import views
from . import views
from django.urls import path
from . import views


urlpatterns=[
  url(r'^meet_collegues/$', views.meet_collegues, name = 'meet_collegues'),
  url(r'^single_idea/(\d+)/$', views.single_idea, name = 'single_idea'),
 
  path("",views.index,name="index"),
  path("story/",views.create_story,name="story"),
  url(r'discussion', views.Discussion, name='discussion'),
  url(r'fundraiser', views.Fundraiser, name='fundraiser'),   
  url(r'^meet_collegues/$', views.meet_collegues, name = 'meet_collegues')

]
if settings.DEBUG:
  urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)