from django.contrib import admin
from .models import BlogContent, PageHeading, BackgroundImage

# Register your models here.
#Headings
admin.site.register(PageHeading)

#Content
admin.site.register(BlogContent)
admin.site.register(BackgroundImage)
