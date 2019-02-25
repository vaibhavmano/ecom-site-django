from django.contrib import admin
from .models import CustomUser, ContactInfo, CustomSeller

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(CustomSeller)
admin.site.register(ContactInfo)