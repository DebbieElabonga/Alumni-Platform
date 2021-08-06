from django.contrib import admin
from .models import Message, Stories,UserProfile,Tech , GeneralAdmin
# Register your models here.

admin.site.register(GeneralAdmin)
admin.site.register(UserProfile)
admin.site.register(Stories)
admin.site.register(Tech)
admin.site.register(Message)
