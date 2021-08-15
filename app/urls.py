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

  # url(r'fundraiser', views.Fundraiser, name='fundraiser'),   
  url(r'^meet_collegues/$', views.meet_collegues, name = 'meet_collegues'),


  url(r'^$',views.index,name="index"),

#user authentication urls-------------------------------------------------------------------------------
  # url(r'^register/$',views.signup, name='registration'),
  url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
  url(r'^logout/$',auth_views.LogoutView.as_view(), name='logout'),

#User Oriented Views ------------------------------------------------------------------------------
  url(r'^user_profile/$', views.profile, name='user_profile'),
  url(r'^meet_collegues/$', views.meet_collegues, name = 'meet_collegues'),
  url(r'^single_idea/(\d+)/$', views.single_idea, name = 'single_idea'),
  url(r'^story/$',views.create_story,name='story'),

  url(r'^edit_creds/$', views.edit_details, name = 'edit_creds'),
  
  

# Admin oriented views------------------------------------------------------------------------------ 
  url(r'^admin_dashboard/$', views.summary, name = 'admin_dashboard'),
  url(r'^new_cohort/$', views.cohort, name='new_cohort'),
  url(r'^fundraiser/$', views.Fundraiser, name='fundraiser'),   
  
  #url(r'^admin_dashboard/$', views.admin_dashboard, name = 'admin_dashboard'),
  path("story/",views.create_story,name="story"),
  url(r'^new_cohort/$', views.cohort, name='new-cohort'),
  path('discussion/<int:id>/', views.Discussion, name='discussion'),
  path('cohort/<int:id>/', views.cohortdiscussions, name = 'cohortdiscussions'),
  path('reply/<int:id>/', views.reply, name = 'reply'),
  url(r'fundraiser', views.Fundraiser, name='fundraiser'),   
  path("news/",views.TechNews,name="technews"),
  # url(r'^create_user/$',user_views.create_user,name='create_user'),
  path('invitation/<uidb64>/<token>',  views.InviteUserView.as_view(), name='invitation'),
  url(r'^discussion/$', views.Discussion, name='discussion'),
  # # url(r'^create_user/$',user_views.create_user,name='create_user'),
  # path('invitation/<uidb64>/<token>',  views.InviteUserView.as_view(), name='invitation'),
  url(r'^invite_members/$', views.invite_members, name = 'invite_members'),
  path('invitation/<uidb64>/<token>',  views.InviteUserView.as_view(), name='invitation'),
  path('download_csv/', views.download_csv, name = 'download_csv'),

  url(r"^story/",views.create_story,name="story"),
  url(r'^new_cohort/$', views.cohort, name='new-cohort'),
  url(r'^fundraiser', views.Fundraiser, name='fundraiser'),   
  path("joincohort/<int:id>/",views.joincohort,name="joincohort"),
  path("leavecohort/<int:id>/",views.leavecohort,name="leavecohort"),
  path('post/ajax/close_project', views.close_project, name='close_project')
  
]
if settings.DEBUG:
  urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)