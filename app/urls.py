from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path


urlpatterns=[
  path("",views.index,name="index"),
  path("story/",views.create_story,name="story"),
  path("technews/",views.add_tech_news,name="technews"),

]
if settings.DEBUG:
  urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)