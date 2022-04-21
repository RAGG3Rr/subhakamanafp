from django.db import models

# Create your models here.

class Catelogue(models.Model):
  name = models.CharField(max_length=50)
  description = models.CharField(max_length=500)
  file = models.FileField(upload_to='catelogue_files')

  def __str__(self):
      return self.name
  