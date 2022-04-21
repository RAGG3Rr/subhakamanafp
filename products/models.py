from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
#from .utils import unique_slug_generator
import string 
from django.utils.text import slugify 
import random 

# Create your models here.

class Colors(models.Model):
    name = models.CharField(max_length=100,null = True, blank = True)
    
    def __str__(self):
        return self.name



class Category(models.Model):
    main_category = models.CharField(max_length=50, unique=True)
    display = models.BooleanField()
    slug = models.SlugField(max_length = 200, null = True, blank = True)
    class Meta:
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.main_category
    
def random_string_generator(size = 10, chars = string.ascii_lowercase + string.digits): 
    return ''.join(random.choice(chars) for _ in range(size)) 
  
def unique_categoryslug_generator(instance, new_slug = None): 
    if new_slug is not None: 
        slug = new_slug 
    else: 
        slug = slugify(instance.main_category) 
    Klass = instance.__class__ 
    qs_exists = Klass.objects.filter(slug = slug).exists() 
      
    if qs_exists: 
        new_slug = "{slug}-{randstr}".format( 
            slug = slug, randstr = random_string_generator(size = 4)) 
              
        return unique_categoryslug_generator(instance, new_slug = new_slug) 
    return slug 

def pre_save_receiver_categories(sender, instance, *args, **kwargs): 
   if not instance.slug: 
       instance.slug = unique_categoryslug_generator(instance) 

pre_save.connect(pre_save_receiver_categories, sender = Category)
    
        
class SubCategory(models.Model):
    main_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.CharField(max_length=50, unique=False)
    Add_features = models.BooleanField(null=True,blank=True,default=True)
    slug = models.SlugField(max_length = 200, null = True, blank = True)
    class Meta:
        verbose_name_plural = 'sub-categories'

    def __str__(self):
        return f'{self.sub_category} - {self.main_category}'

def unique_subcategoryslug_generator(instance, new_slug = None): 
    if new_slug is not None: 
        slug = new_slug 
    else: 
        slug = slugify(instance.sub_category) 
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

pre_save.connect(pre_save_receiver_subcategories, sender = SubCategory)

class SpecificCategory(models.Model):
    main_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    specific_category = models.CharField(max_length=50, unique=False)
    slug = models.SlugField(max_length = 200, null = True, blank = True)
    class Meta:
        verbose_name_plural = 'specific-categories'

    def __str__(self):
        return f'{self.specific_category} - {self.sub_category.sub_category} - {self.main_category}'

def unique_specificslug_generator(instance, new_slug = None): 
    if new_slug is not None: 
        slug = new_slug 
    else: 
        slug = slugify(instance.specific_category) 
    Klass = instance.__class__ 
    qs_exists = Klass.objects.filter(slug = slug).exists() 
      
    if qs_exists: 
        new_slug = "{slug}-{randstr}".format( 
            slug = slug, randstr = random_string_generator(size = 4)) 
              
        return unique_specificslug_generator(instance, new_slug = new_slug) 
    return slug 

def pre_save_receiver_specificcategories(sender, instance, *args, **kwargs): 
   if not instance.slug: 
       instance.slug = unique_specificslug_generator(instance) 

pre_save.connect(pre_save_receiver_specificcategories, sender = SpecificCategory)

class SaleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(on_sale=False)

class Product(models.Model):
    main_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    specific_category = models.ForeignKey(SpecificCategory, on_delete=models.CASCADE, null=True, blank=True)
    product_title = models.CharField(max_length = 255)
    description = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to='product_image')
    price = models.DecimalField(max_digits=20,decimal_places=2,blank=True, null=True)
    items_in_stock = models.IntegerField(blank=True, null=True, default = 0)
    added_date=models.DateTimeField(auto_now_add=True,null=True)
    on_sale = models.BooleanField(default= False)
    colors = models.CharField(max_length=64,blank=True, null=True)
    slug = models.SlugField(max_length = 200, null = True, blank = True)

    objects = models.Manager()
    nosale = SaleManager()

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.product_title

    def remove_on_image_update(self):
        try:
            obj = Product.objects.get(id=self.id)
        except Product.DoesNotExist:
            return
        if obj.image and self.image and obj.image != self.image:
            obj.image.delete()

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.remove_on_image_update()
        return super(Product, self).save(*args, **kwargs)
def unique_productslug_generator(instance, new_slug = None): 
    if new_slug is not None: 
        slug = new_slug 
    else: 
        slug = slugify(instance.product_title) 
    Klass = instance.__class__ 
    qs_exists = Klass.objects.filter(slug = slug).exists() 
      
    if qs_exists: 
        new_slug = "{slug}-{randstr}".format( 
            slug = slug, randstr = random_string_generator(size = 4)) 
              
        return unique_productslug_generator(instance, new_slug = new_slug) 
    return slug 

def pre_save_receiver_product(sender, instance, *args, **kwargs): 
   if not instance.slug: 
       instance.slug = unique_productslug_generator(instance) 

pre_save.connect(pre_save_receiver_product, sender = Product)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    image = models.ImageField(upload_to="product_image", blank=True, null = True)

    def __str__(self):
        return self.product.product_title

    def remove_on_image_update(self):
        try:
            obj = ProductImage.objects.get(id=self.id)
        except ProductImage.DoesNotExist:
            return
        if obj.image and self.image and obj.image != self.image:
            obj.image.delete()

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.remove_on_image_update()
        return super(ProductImage, self).save(*args, **kwargs)

# class Size

class Mobilememory(models.Model):
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=20,decimal_places=2)
    retailprice =  models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    wholesaleprice = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    size = models.CharField(max_length = 100, null = True, blank = True)
    qty = models.IntegerField(null = True, blank = True)
    product = models.ForeignKey(Product, on_delete = models.CASCADE,blank=True, null=True)
    
    def __str__(self):
        return self.description		
	

class SpecialDeals(models.Model):
    product = models.OneToOneField(Product, on_delete = models.CASCADE)
    productsize = models.ForeignKey(Mobilememory, on_delete=models.CASCADE,null=True)
    discounted_price = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    retail_discount_price = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    discount_percentage=models.FloatField(null=True,blank=True)
    no_of_days=models.IntegerField(null=True,blank=True)
    # added_date=models.DateTiemField(_("Date"), default=datetime.date.today)
    added_date=models.DateTimeField(auto_now_add=True,null=True)
    class Meta:
        verbose_name_plural = 'Special Deals'
 
    def __str__(self):
        return self.product.product_title

class Specialdealattr(models.Model):
    specialdeal = models.ForeignKey(SpecialDeals, on_delete = models.CASCADE)
    productsize = models.ForeignKey(Mobilememory, on_delete=models.CASCADE,null=True)
    discounted_price = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    retail_discount_price = models.DecimalField(max_digits=20,decimal_places=2, null=True)

    class Meta:
        verbose_name_plural = 'Special Deal Attr'
 
    def __str__(self):
        return f'{self.productsize}'

class Poster(models.Model):
    image = models.ImageField(upload_to="product_image", blank=True, null = True)
    extra_link = models.CharField(max_length=100,null=True,blank=True)
    def remove_on_image_update(self):
        try:
            obj = Poster.objects.get(id=self.id)
        except Poster.DoesNotExist:
            return
        if obj.image and self.image and obj.image != self.image:
            obj.image.delete()

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.remove_on_image_update()
        return super(Poster, self).save(*args, **kwargs)

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True)
    transaction_id = models.CharField(max_length=200, null=True)
    sessionid=models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems=self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems=self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)  
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)  
    quantity = models.IntegerField(default=0, blank=True, null=True)  
    date_added = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=20,decimal_places=2,null=True, blank=True, default=0)
    sessionid=models.IntegerField(null=True, blank=True)
    colors = models.CharField(max_length=64,blank=True, null=True)
    features = models.CharField(max_length = 64,blank=True, null=True)
    def __str__(self):
        return str(self.product)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length = 255)
    city = models.CharField(max_length = 255)
    state = models.CharField(max_length = 255)
    zipcode = models.CharField(max_length = 255)
    phone = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Shipping Address'

    def __str__(self):
        return self.address

STATUS = (
    ("Pending", "Pending"),
    ("Received", "Received"),
    ("Out for Delivery", "Out for Delivery"),
    ("Delivered", "Delivered"),
)

class ShippingCharges(models.Model):
    charges = models.DecimalField(max_digits=20,decimal_places=2)

    def __str__(self):
        return str(self.charges)

class OrderStatus(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    order_status = models.CharField(max_length = 30, choices = STATUS, default = 'Pending')
    
    def __str__(self):
        return self.order_status

    class Meta:
        verbose_name_plural = 'Order Status'

PAYMENT = (
    ("Cash On Delivery", "Cash On Delivery"),
    ("Paid", "Paid"),
    ("due", "due"),
)

class PaymentMedium(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    payment_mode = models.CharField(max_length = 100)

    class Meta:
        verbose_name_plural = 'Payment Mode'

    def __str__(self):
        return self.payment_mode

class Add_payment_types(models.Model):
    payment_name = models.CharField(max_length = 100)
    payment_id = models.IntegerField()
    image=models.ImageField(upload_to='payment_images')
    
    def __str__(self):
        return self.payment_name		
		
class Size(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    small = models.BooleanField()
    medium = models.BooleanField()
    large = models.BooleanField()

class Review(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(default = 1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.CharField(max_length=500)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.rating}-{self.user}'

class Trending(models.Model):
    product = models.OneToOneField(Product, on_delete = models.CASCADE)

    def __str__(self):
        return self.product.product_title

class Slideshow(models.Model):
    image = models.ImageField(upload_to="slideshow_images")
    extra_link = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.image.url

    def remove_on_image_update(self):
        try:
            obj = Slideshow.objects.get(id=self.id)
        except Slideshow.DoesNotExist:
            return
        if obj.image and self.image and obj.image != self.image:
            obj.image.delete()

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.remove_on_image_update()
        return super(Slideshow, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Slideshow Images'

class CustomTable(models.Model):
    product = models.OneToOneField(Product, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.product.product_title

    class Meta:
        verbose_name_plural = 'Custom Table Items'

class CustomTableName(models.Model):
    table_title = models.CharField(max_length=500)

    def __str__(self):
        return self.table_title
