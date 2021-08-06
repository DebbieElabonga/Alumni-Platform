from django.contrib import admin

from .models import (Fundraiser, Message,GeneralAdmin, Tech,UserProfile,Stories,TechNews)

# Register your models here.
admin.site.register(Fundraiser)
admin.site.register(Message)



admin.site.register(GeneralAdmin)
admin.site.register(UserProfile)
admin.site.register(Stories)
admin.site.register(Tech)
admin.site.register(Message)
