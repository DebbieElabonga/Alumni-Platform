from django.contrib import admin

from .models import (Fundraiser, Message)

# Register your models here.
admin.site.register(Fundraiser)
admin.site.register(Message)


