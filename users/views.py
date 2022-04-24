from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm,CompanyProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from allauth.account.views import PasswordSetView
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.urls import reverse_lazy
from products.models import *
from .models import *

# Create your views here.
def adduser(request):
    
	pass

def registerIndividual(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            email = request.POST['email']
            contact = request.POST['contact']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            purpose = request.POST['purpose'] or ""
            city = request.POST['city'] or None;
            address = request.POST['address']
            province = request.POST['province'] or None;
            zipcode = request.POST['zipcode'] or None;


            if first_name != '' and last_name != '' and username != '' and email != '' and password1 != '' and contact != '' and address != '':
                if password1 == password2:
                    if User.objects.filter(username=username).exists():
                        messages.info(request, 'Username already taken')
                    elif User.objects.filter(email=email).exists():
                        messages.info(request, 'Email already taken')
                    elif Profile.objects.filter(phone_no=contact).exists():
                        messages.info(request, 'Phone Number already taken')
                    else:
                        confirmationIndividualEmail(request,f'{first_name} {last_name}',email)

                        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username,
                                                        password=password1, email=email)
                        user.save()
                        detail = Profile(user=user,phone_no=contact,address=address,city=city,state=province,zipcode=zipcode,purpose=purpose)
                        detail.save()
                        messages.info(request, 'You are registered successfully. You can go head and log in now')
                        return redirect('login')
                else:
                    messages.info(request, 'Your password is not matching')
            else:
                messages.info(request, 'Required field cannot be empty! Please fill up required fields')


    return render(request, 'users/companyregister.html')

def registerorganization(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            email = request.POST['email']
            contact = request.POST['contact']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            purpose = request.POST['purpose'] or ""
            city = request.POST['city'] or None;
            address = request.POST['address'] or None;
            province = request.POST['province'] or None;
            zipcode = request.POST['zipcode'] or None;
            companyname = request.POST['company_name'];
            companyweb = request.POST['company_website'] or None;
            usertype = request.POST['user_type'] or None;

            if usertype == 'Wholesaler' or usertype == 'Retailer':
                usertype = usertype
            else:
                return redirect('register')

            if first_name != '' and last_name != '' and username != '' and email != '' and contact != '' and address != '' and password1 != '' and companyname != '':
                if password1 == password2:
                    if User.objects.filter(username=username).exists():
                        messages.info(request, 'Username already taken')
                    elif User.objects.filter(email=email).exists():
                        messages.info(request, 'Email already taken')
                    else:
                        confirmationOrganizationEmail(request,f'{first_name} {last_name}',email,usertype)

                        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username,
                                                        password=password1, email=email,is_active=False)
                        user.save()
                        profile = Profile(user=user,user_type=usertype,phone_no=contact,address=address,city=city,state=province,zipcode=zipcode,company_name=companyname,company_website=companyweb,purpose=purpose)
                        profile.save()
                        userconfirmationEmail(request,f'{first_name} {last_name}',usertype,profile.id)

                        messages.info(request, 'You are registered successfully. You will get registration approval request.')
                        return redirect('login')
                else:
                    messages.info(request, 'Your password is not matching')
            else:
                messages.info(request, 'Required field cannot be empty! Please fill up required fields')


    return render(request, 'users/companyregister.html')


@login_required
def profile(request):
    orders = Order.objects.filter(customer_id = request.user.id)
    customer_order = []
    for order in orders:
        if order.complete == True:
            customer_order.append(order)
        
    order_status = OrderStatus.objects.all()

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile has been updated.')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        password_reuse = request.user.has_usable_password()
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context={
        'u_form':u_form,
        'p_form': p_form,
        'password_reuse':password_reuse,
        'customer_order':customer_order,
        'order_status':order_status,
    }

    return render(request, 'users/profile.html', context)

def DeleteProfile(request, pk):
    u_id = request.user.id
    profile_uid = User.objects.get(id = pk)
    p_id = profile_uid.id
    if request.method == 'POST':
        if p_id == u_id:
            profile_uid.delete()
            logout(request)
            messages.success(request, f'User has been deleted.')
            return redirect('register')
    else:
        messages.error(request, f'You are not authorized to delete users!')
        return redirect('profile')

class MyPasswordSetView(PasswordSetView):
    success_url = reverse_lazy('profile')

def checkPassword(request):
    if request.user.is_authenticated:
        password_reuse = request.user.has_usable_password()
    else:
        password_reuse = True
    return{
        'password_reuse':password_reuse,
    }

def confirmationIndividualEmail(request,name, mailaddress):
    current_site = get_current_site(request)
    template = render_to_string('users/messages/register_individualemail.html', {'name': name,'current_site':current_site})
    try:
        email = EmailMessage(
            'User registerd!',
            template,
            settings.EMAIL_HOST_USER,
            [mailaddress],
        )
        email.fail_silently = False
        email.send()
    except:
         messages.error(request, f'Enter a valid Email address.')
         return redirect("register")

def confirmationOrganizationEmail(request,name, mailaddress,usertype):
    current_site = get_current_site(request)
    template = render_to_string('users/messages/register_Organizationemail.html', {'name': name,'current_site':current_site,'usertype':usertype})
    try:
        email = EmailMessage(
            'Registraion Alert!',
            template,
            settings.EMAIL_HOST_USER,
            [mailaddress],
        )
        email.fail_silently = False
        email.send()
    except:
        messages.error(request, f'Enter a valid Email address.')
        return redirect("register")

def userconfirmationEmail(request,name,usertype,id):
    current_site = get_current_site(request)
    template = render_to_string('users/messages/userconfirmation.html', {'name': name,'current_site':current_site,'usertype':usertype,'id':id})
    try:
        email = EmailMessage(
            f'{usertype} User Registred!',
            template,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
        )
        email.fail_silently = False
        email.send()
    except:
        pass


# def myInvoice(request):
#     orders = Order.objects.filter(customer_id = request.user.id)
#     customer_order = []
#     for order in orders:
#         if order.complete == True:
#             customer_order.append(order)
        
#     order_status = OrderStatus.objects.all()

#     context={
#         'customer_order':customer_order,
#         'order_status':order_status,
#     }

#     return render(request,"users/myinvoice",context)

