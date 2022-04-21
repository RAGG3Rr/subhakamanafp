from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'opening',"salary","end_date"]
    list_editable = ['opening','salary']
    search_fields = ['title']
    exclude = ('slug',)

@admin.register(ApplyJob)
class ApplyJobAdmin(admin.ModelAdmin):
    list_display = ['get_job', 'full_name','email']
    search_fields = ['get_job__title']