from django.db import models

# Create your models here.
class FAQ(models.Model):
    question = models.CharField(max_length = 500)
    answer = models.TextField(max_length=1500)

    def __str__(self):
        return f'{self.question}'