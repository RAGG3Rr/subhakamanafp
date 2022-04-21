from django.db import models
from django.template.defaultfilters import slugify
from django.utils.text import slugify 
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
import string 
import random 

class Job(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    slug = models.SlugField(max_length = 200, null = True, blank = True)
    opening=models.IntegerField()
    start_date=models.DateField()
    end_date=models.DateField()
    salary=models.CharField(max_length=50)
    experiance=models.CharField(max_length=255)
    location=models.CharField(max_length=100)
    skill=models.CharField(max_length=255)
    description=models.CharField(max_length=300)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name_plural = 'Vacancies'

    def clean(self):
        start_date = self.start_date
        end_date = self.end_date
        if (start_date > end_date):
            raise ValidationError(
                {'end_date': "End date should be greater than start date"})

def random_string_generator(size = 10, chars = string.ascii_lowercase + string.digits): 
    return ''.join(random.choice(chars) for _ in range(size)) 

def unique_subcategoryslug_generator(instance, new_slug = None): 
    if new_slug is not None: 
        slug = new_slug 
    else: 
        slug = slugify(instance.title) 
    Klass = instance.__class__ 
    qs_exists = Klass.objects.filter(slug = slug).exists() 
      
    if qs_exists: 
        new_slug = "{slug}-{randstr}".format( 
            slug = slug, randstr = random_string_generator(size = 4)) 
              
        return unique_subcategoryslug_generator(instance, new_slug = new_slug) 
    return slug 

def pre_save_receiver_subcategories(sender, instance, *args, **kwargs): 
   if not instance.slug: 
       instance.slug = unique_subcategoryslug_generator(instance) 

pre_save.connect(pre_save_receiver_subcategories, sender = Job)

class ApplyJob(models.Model):
	id=models.AutoField(primary_key=True)
	get_job=models.ForeignKey(Job, on_delete=models.CASCADE)
	full_name=models.CharField(max_length=50)
	birth=models.DateField()
	email=models.EmailField(max_length=255)
	phone=models.IntegerField()
	cv=models.FileField(upload_to="vacancy/cv")
	cover_letter=models.FileField(upload_to="vacancy/coverletter")
	hear=models.CharField(max_length=255)
	refer=models.CharField(max_length=255)
	next_role=models.CharField(max_length=255)
	offer=models.DateField()