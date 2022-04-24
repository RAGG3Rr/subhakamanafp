from ast import mod
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from .helpers import accountverificationmail

USER_TYPE = (
    ('Normal','Normal'),
    ('Wholesaler','Wholesaler'),
    ('Retailer','Retailer')
)

APPROVE_USER = (
    ('None','None'),
    ('Approve as Wholesaler','approveWholesaler'),
    ('Approve as Retailer','approveRetailer')
)

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length = 30, choices = USER_TYPE, default = 'Normal')
    image = models.ImageField(default='default.jpg', upload_to='profile-pics')
    phone_no=models.IntegerField(null=True,blank=True)
    address = models.CharField(max_length = 255,null=True,blank=True)
    city = models.CharField(max_length = 255,null=True, blank=True)
    state = models.CharField(max_length = 255, null=True,blank=True)
    zipcode = models.CharField(max_length = 255,null=True, blank=True)
    company_name = models.CharField(max_length=255, default='',null=True,blank=True)
    company_website = models.CharField(max_length=255, default='',null=True,blank=True)
    purpose = models.CharField(max_length=255, default='',null=True,blank=True)
    approveWholesaler = models.BooleanField(default=False)
    approveRetailer = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True,blank=True,null=True)
	
    def remove_on_image_update(self):
        try:
            obj = Profile.objects.get(id=self.id)
        except Profile.DoesNotExist:
            return
        
        if obj.image != "default.jpg":
            if obj.image and self.image and obj.image != self.image:
                obj.image.delete()
    
    def approveuser(self):
        getwholesaler = self.approveWholesaler
        getRetailer = self.approveRetailer
        old_object_instance = Profile.objects.get(pk=self.pk)
        oldwholesale = old_object_instance.approveWholesaler
        oldretaile = old_object_instance.approveRetailer

        if not oldwholesale == True and oldretaile == False:
            if getwholesaler == True and getRetailer == False:
                User.objects.filter(username = self.user).update(is_active = True)
                accountverificationmail(f'{self.user.first_name} {self.user.last_name}',self.user.email,self.user_type)
            else:
                User.objects.filter(username = self.user).update(is_active = False)

        if not oldretaile == True and oldwholesale == False:
            if getwholesaler == False and getRetailer == True:
                User.objects.filter(username = self.user).update(is_active = True)
                accountverificationmail(f'{self.user.first_name} {self.user.last_name}',self.user.email,self.user_type)
            else:
                User.objects.filter(username = self.user).update(is_active = False)


    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs) 

    def save(self, *args, **kwargs):
        self.remove_on_image_update()
        try:
            self.approveuser()
        except:
            pass
        return super(Profile, self).save(*args, **kwargs)

    def User_name(self):
        username = f'{self.user.first_name} {self.user.last_name}'
        return username
    
    def Confirm_Wholesaler_Retailer(self):
        approvedRetailer = self.approveRetailer
        approvedWholesaler = self.approveWholesaler

        if not self.user_type == 'Normal':
            if approvedRetailer == True or approvedWholesaler == True:
                show = 'Confirmed'
            else:
                show = 'Not Confirmed'
        else:
            show = '-'

        return show
    
    def Company_name(self):
        if self.user_type == 'Normal':
            type = '-'
        else:
            type = self.company_name
        return type

############################################################################################

class Subscription(models.Model):
    email = models.CharField(max_length=255)
    status = models.CharField(max_length=255)

    def __str__(self):
        return self.email


class ComposeEmail(models.Model):
    subject = models.CharField(max_length=255)
    content = models.CharField(max_length=2058)
    image = models.ImageField(upload_to='img/mail_image', default="", null=True)

    def __str__(self):
        return self.subject
