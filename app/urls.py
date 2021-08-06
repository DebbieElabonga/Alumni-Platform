from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path

urlpatterns=[
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
  url(r'^discussion/$', views.Discussion, name='discussion'),
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