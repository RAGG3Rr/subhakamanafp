from django.contrib import admin
from .models import Profile 

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['User_name','phone_no','Company_name','user_type','Confirm_Wholesaler_Retailer']
    search_fields = ['user_type']
    ordering = ("-user_type",)
    class Media:
        js = ("js/profile.js",)
