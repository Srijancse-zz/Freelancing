from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=11)
    address = models.TextField()
