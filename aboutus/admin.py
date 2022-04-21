from django.contrib import admin
from .models import Heading, Customer_view, OurTeam, OurClients,Userquery,Contact
from django.forms import TextInput, Textarea
from django.db import models

# Register your models here.
#Headings
admin.site.register(Heading)

#Content
admin.site.register(Customer_view)
admin.site.register(OurTeam)
admin.site.register(OurClients)
admin.site.register(Userquery)
# admin.site.register(Contact)



class ContactModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'40'})},
        models.IntegerField: {'widget': TextInput(attrs={'size':'40'})},
        # models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }

admin.site.register(Contact, ContactModelAdmin)