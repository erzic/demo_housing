from django.db import models

# Create your models here.

class houses(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField()
    location = models.CharField(max_length=200)
    size = models.FloatField(max_length=200)