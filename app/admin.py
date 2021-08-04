from app.models import GeneralAdmin, UserProfile
from django.contrib import admin
from .models import Stories,UserProfile,TechNews
# Register your models here.

admin.site.register(GeneralAdmin)
admin.site.register(UserProfile)
admin.site.register(Stories)
admin.site.register(TechNews)
