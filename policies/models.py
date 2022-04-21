from django.db import models

# Create your models here.
class PrivacyPolicy(models.Model):
    title = models.CharField(max_length=1000, blank=True)
    content = models.TextField(max_length=4000)
    
    def __str__(self):
      if self.title:
        return (f'{self.title}')
      else:
        return (f'object-{self.id}')

    class Meta:
        verbose_name_plural = 'Privacy Policies'

class Exchange(models.Model):
  title = models.CharField(max_length=255, blank=True)
  description = models.TextField()

  class Meta:
      verbose_name_plural = "Return Policies" 

  def __str__(self):
    if self.title:
      return (f'{self.title}')
    else:
      return (f'object-{self.id}')