from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import HttpResponse

def accountverificationmail(name, mailaddress,usertype):
    current_site = Site.objects.get(id= 4)
    template = render_to_string('users/messages/accountverificationmessage.html', {'name': name,'current_site':current_site,'usertype':usertype})
    # try:
    email = EmailMessage(
        'Account Verified!',
        template,
        settings.EMAIL_HOST_USER,
        [mailaddress],
    )
    email.fail_silently = False
    email.send()

    print("hello")
    # except:
    #     print("wrong")
    #     HttpResponse("Something went wrong.")