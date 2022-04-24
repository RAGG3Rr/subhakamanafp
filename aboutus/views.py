from django.shortcuts import render,redirect
from .models import Heading, Customer_view, OurTeam, OurClients,Contact,Userquery,Newsletter
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
# Create your views here.

def about(request):
    template = "aboutus/about.html"
    
    heading = Heading.objects.all()
    clients = OurClients.objects.all()
    review = Customer_view.objects.all()[:4]
    team = OurTeam.objects.all()
    context={
        'heading': heading,
        'team':team,        
        'clients':clients,      
        'review':review,        
    }
    return render(request, template,context)

def teams(request):
    template = "aboutus/team.html"
    
    team = OurTeam.objects.all()
    context={
        'team':team,        
    }
    return render(request, template,context)

def client(request):
    template = "aboutus/client.html"
    
    clients = OurClients.objects.all()
    review = Customer_view.objects.all()[:4]
    context={
        'clients':clients,      
        'review':review,        
    }
    return render(request, template,context)


def contactus(request):
    template = "aboutus/contact.html"
    
    #print('reached here')
    if request.method=='POST':
        firstname=request.POST.get("firstname", "")
        lastname=request.POST.get('lastname','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        subject=request.POST.get('subject','')
        message=request.POST.get('message','')
        
        Userquery.objects.create(firstname=firstname,
        lastname=lastname,
        email=email,
        phone_no=phone,
        subject=subject,
        message=message,
        )
        confirmationEmail(request,firstname,lastname,phone,email,subject,message)
        messages.success(request, 'Thanks for submitting your query!!')
        return render(request,template)
    return render(request,template)

def newsletter(request):
    if request.method == 'POST':
        if request.POST.get('email'):
            email= request.POST.get('email')
            news= Newsletter.objects.create(email = email)
            news.save()
            messages.success(request, 'Subscribed Successfully')
            return redirect('home') 
        else:
            messages.error(request, 'Cannot Subscribe')
            return redirect('home') 
    else:
        return render(request,'base.html')

def confirmationEmail(request,firstname,lastname,phone,cont_email,subject,message):
    template = render_to_string('aboutus/userquery_email.html', {
        'firstname': firstname,
        'lastname':lastname,
        "phone":phone,
        'email':cont_email,
        'subject':subject,
        'message':message
        })
    email = EmailMessage(
        f'Message from {firstname} {lastname}',
        template,
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_HOST_USER],
    )
    email.fail_silently = False
    email.send()

