from django.contrib import admin
from .models import CustomUser, ContactInfo, CustomSeller, OrderInfo

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(CustomSeller)
admin.site.register(ContactInfo)
admin.site.register(OrderInfo)
class OrderInfoAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request))
        if not request.user.is_superuser:
            fields.append('orderstatus')
        return fields 

admin.site.site_header = 'E-Commerce'