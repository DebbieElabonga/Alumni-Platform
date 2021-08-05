from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path
from . import views

urlpatterns=[
  url(r"",views.index,name="index"),
  url(r'register/',views.signup, name='registration'),
  url(r'login/', auth_views.LoginView.as_view(), name='login'),
  url(r'logout/',auth_views.LogoutView.as_view(), name='logout'),
  url(r'profile/', views.profile, name='profile'),
  url(r'new-cohort/', views.cohort, name='new-cohort'),
  url(r'^meet_collegues/$', views.meet_collegues, name = 'meet_collegues'),
  url(r'^single_idea/(\d+)/$', views.single_idea, name = 'single_idea'),
  url(r"story/",views.create_story,name="story"),
  url(r'discussion', views.Discussion, name='discussion'),
  url(r'fundraiser', views.Fundraiser, name='fundraiser'),   
  url(r'^meet_collegues/$', views.meet_collegues, name = 'meet_collegues'),
  url(r"news/",views.TechNews,name="technews"),
  url(r'^admin_dashboard/$', views.summary, name = 'admin_dashboard'),
]
if settings.DEBUG:
  urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)