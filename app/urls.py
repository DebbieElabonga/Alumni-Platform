from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path


urlpatterns=[
    url(r'^$',views.index,name='index'),
    url('register/',views.signup, name='registration'),
    url('login/', auth_views.LoginView.as_view(), name='login'),
    url('logout/',auth_views.LogoutView.as_view(), name='logout'),
    url('profile/', views.profile, name='profile'),
    url('new-cohort/', views.cohort, name='new-cohort'),
    path('joincohort/<id>', views.join_cohort, name='joincohort'),
    path('leave_cohort/<id>', views.leave_cohort, name='leave-cohort'),
]
if settings.DEBUG:
  urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)