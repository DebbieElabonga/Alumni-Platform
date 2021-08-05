from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from django.urls.conf import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns=[
    path('', views.index, name="index"),
    path('charge/', views.charge, name="charge"),
    path('success/<str:args>/', views.successMsg, name="success"),

  path("",views.index,name="index"),
  url('register/',views.signup, name='registration'),
  url('login/', auth_views.LoginView.as_view(), name='login'),
  url('logout/',auth_views.LogoutView.as_view(), name='logout'),
  url('profile/', views.profile, name='profile'),
  url('new-cohort/', views.cohort, name='new-cohort'),
  url(r'^meet_collegues/$', views.meet_collegues, name = 'meet_collegues'),
  url(r'^single_idea/(\d+)/$', views.single_idea, name = 'single_idea'),
  # url(r'^admin_dashboard/$', views.admin_dashboard, name = 'admin_dashboard'),
  url("story/",views.create_story,name="story"),
  url(r'discussion', views.Discussion, name='discussion'),
  # url(r'fundraiser', views.Fundraiser, name='fundraiser'),   
  url(r'^meet_collegues/$', views.meet_collegues, name = 'meet_collegues'),
  path("news/",views.TechNews,name="technews"),
  url(r'^admin_dashboard/$', views.summary, name = 'admin_dashboard'),
]
if settings.DEBUG:
  urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)