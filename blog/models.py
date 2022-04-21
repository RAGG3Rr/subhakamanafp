from django.db import models
from django.utils import timezone
from PIL import Image

# Create your models here.
class PageHeading(models.Model):
    page_heading = models.CharField(max_length=80)

    def __str__(self):
        return f'{self.page_heading}'

class BackgroundImage(models.Model):
    background_image = models.ImageField(upload_to="background_images")

    def remove_on_image_update(self):
        try:
            obj = BackgroundImage.objects.get(id=self.id)
        except BackgroundImage.DoesNotExist:
            return

        if obj.background_image and self.background_image and obj.background_image != self.background_image:
            obj.background_image.delete()

    def delete(self, *args, **kwargs):
        self.background_image.delete()
        super().delete(*args, **kwargs) 

    def save(self, *args, **kwargs):
        self.remove_on_image_update()
        return super(BackgroundImage, self).save(*args, **kwargs)
        
class BlogContent(models.Model):
    blog_title = models.CharField(max_length=200)
    blog_content = models.TextField(max_length=2000)
    blog_img = models.ImageField(upload_to="blog_images")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.blog_title}'

    def remove_on_image_update(self):
        try:
            obj = BlogContent.objects.get(id=self.id)
        except BlogContent.DoesNotExist:
            return
            
        if obj.blog_img and self.blog_img and obj.blog_img != self.blog_img:
            obj.blog_img.delete()

    def delete(self, *args, **kwargs):
        self.blog_img.delete()
        super().delete(*args, **kwargs) 

    def save(self, *args, **kwargs):
        self.remove_on_image_update()
        return super(BlogContent, self).save(*args, **kwargs)
