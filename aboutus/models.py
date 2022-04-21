from django.db import models
from django.utils import timezone
from PIL import Image

# Create your models here.
class Heading(models.Model):
    title = models.CharField(max_length=80)
    content = models.TextField()
    title_image = models.ImageField(upload_to="aboutus_images")
    def __str__(self):
        return f'{self.title}'

class Newsletter(models.Model): 
    email = models.EmailField(null=True)
    number = models.CharField(max_length=15)

    def __str__(self):
        return f'{self.email}'

class Customer_view(models.Model):
    review = models.TextField()
    review_by = models.CharField(max_length=80)
    
    def __str__(self):
        return f'{self.review}'     
        
class OurTeam(models.Model):
    name=models.CharField(max_length=64)
    designation=models.CharField(max_length=64)
    short_description=models.CharField(max_length=64)
    email=models.CharField(max_length=64)
    upload_image = models.ImageField(upload_to="aboutus_images")

    def __str__(self):
        return f'{self.name}'
        
class OurClients(models.Model):
    company_name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="aboutus_images")

    def __str__(self):
        return f'{self.company_name}'

class Contact(models.Model):
    outlet = models.CharField(max_length=255, null=True, blank=True)
    title= models.CharField(max_length=255, null=True, blank=True)
    Location = models.CharField(max_length=80,null=True,blank=True)
    phone_no1 = models.IntegerField(null=True,blank=True)
    phone_no2 = models.IntegerField(null=True,blank=True)
    phone_no3 = models.IntegerField(null=True,blank=True)
    link = models.CharField(max_length=255, null=True,blank=True)
    email = models.EmailField(max_length=64)
    def __str__(self):
        return f'{self.Location}'
        
class Userquery(models.Model):
    firstname = models.CharField(max_length=80,null=True,blank=True)
    lastname = models.CharField(max_length=80,null=True,blank=True)
    phone_no = models.CharField(max_length=80,null=True,blank=True)
    email = models.EmailField(max_length=64,null=True,blank=True)
    subject = models.CharField(max_length=80,null=True,blank=True)
    message = models.CharField(max_length=80,null=True,blank=True)
    def __str__(self):
        return f'{self.firstname}'