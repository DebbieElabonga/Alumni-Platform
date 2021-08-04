from django.contrib import admin
from .models import Stories,UserProfile,TechNews , GeneralAdmin
# Register your models here.
admin.site.register(GeneralAdmin)
admin.site.register(UserProfile)
admin.site.register(Stories)
admin.site.register(UserProfile)
admin.site.register(TechNews)
