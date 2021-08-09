from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from django.urls.conf import path
from . import views
from .import views as user_views
from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import path




urlpatterns=[
    # path('', views.donation, name="donation"),
    path('charge/', views.charge, name="charge"),
    path('success/<str:args>/', views.successMsg, name="success"),

  # path("",views.index,name="index"),
  # url('register/',views.signup, name='registration'),
  # url('login/', auth_views.LoginView.as_view(), name='login'),
  # url('logout/',auth_views.LogoutView.as_view(), name='logout'),
  # url('profile/', views.profile, name='profile'),
  # url('new-cohort/', views.cohort, name='new-cohort'),
  # url(r'^meet_collegues/$', views.meet_collegues, name = 'meet_collegues'),
  # url(r'^single_idea/(\d+)/$', views.single_idea, name = 'single_idea'),
  # url(r'^admin_dashboard/$', views.admin_dashboard, name = 'admin_dashboard'),
  url("story/",views.create_story,name="story"),
  url(r'discussion', views.Discussion, name='discussion'),
  # url(r'fundraiser', views.Fundraiser, name='fundraiser'),   
  url(r'^meet_collegues/$', views.meet_collegues, name = 'meet_collegues'),


  url(r'^$',views.index,name="index"),

#user authentication urls-------------------------------------------------------------------------------
  url(r'^register/$',views.signup, name='registration'),
  url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
  url(r'^logout/$',auth_views.LogoutView.as_view(), name='logout'),

#User Oriented Views ------------------------------------------------------------------------------
  url(r'^user_profile/$', views.profile, name='user_profile'),
  url(r'^meet_collegues/$', views.meet_collegues, name = 'meet_collegues'),
  url(r'^single_idea/(\d+)/$', views.single_idea, name = 'single_idea'),
  url(r'^story/$',views.create_story,name='story'),
  url(r'^news/$',views.TechNews,name="technews"),
  
  

# Admin oriented views------------------------------------------------------------------------------ 
  url(r'^admin_dashboard/$', views.summary, name = 'admin_dashboard'),
  url(r'^new_cohort/$', views.cohort, name='new_cohort'),
  url(r'^fundraiser/$', views.Fundraiser, name='fundraiser'),   
  
  #url(r'^admin_dashboard/$', views.admin_dashboard, name = 'admin_dashboard'),
  path("story/",views.create_story,name="story"),
  url(r'^new_cohort/$', views.cohort, name='new-cohort'),
  path('discussion/<int:id>/', views.Discussion, name='discussion'),
  path('all_discussions/<int:id>/', views.all_discussions, name = 'all_discussions'),
  path('reply/<int:id>/', views.reply, name = 'reply'),
  url(r'fundraiser', views.Fundraiser, name='fundraiser'),   
  path("news/",views.TechNews,name="technews"),
  url(r'^discussion/$', views.Discussion, name='discussion'),
  url(r'^create_user/$',user_views.create_user,name='create_user'),
  path('invitation/<uidb64>/<token>',  views.InviteUserView.as_view(), name='invitation'),
  url(r'^invite_members/$', views.invite_members, name = 'invite_members'),
  path('invitation/<uidb64>/<token>',  views.InviteUserView.as_view(), name='invitation'),
  path('download_csv/', views.download_csv, name = 'download_csv'),

  url(r"^story/",views.create_story,name="story"),
  url(r'^new_cohort/$', views.cohort, name='new-cohort'),
  url(r'^discussion', views.Discussion, name='discussion'),
  url(r'^fundraiser', views.Fundraiser, name='fundraiser'),   
  url(r"^news/",views.TechNews,name="technews"),
  
]
if settings.DEBUG:
  urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)