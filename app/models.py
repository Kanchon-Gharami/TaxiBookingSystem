from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import datetime

# User Models...
class myCustomeUser(AbstractUser):
    username = models.CharField(max_length=50, unique="True", blank=False)
    password = models.CharField(max_length=200, blank=False)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=50)
    isCustomer = models.BooleanField(default=False)
    isDriver = models.BooleanField(default=False)
    isAdmin = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Customer(models.Model):
    user = models.OneToOneField(myCustomeUser, null=True, blank=True, on_delete=models.CASCADE)
    paymentMethodCHOICES = [
        ('COD', 'COD'),
    ]
    paymentMethod = models.CharField(max_length=50, choices=paymentMethodCHOICES, default='COD')
    address = models.TextField()

    def __str__(self):
        return self.user.username


class Driver(models.Model):
    user = models.OneToOneField(myCustomeUser, null=True, blank=True, on_delete=models.CASCADE)
    licenseNo = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Trip(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, blank=True, null=True)
    pickup = models.TextField(blank=True, null=True)
    drop = models.TextField(blank=True, null=True)
    pickupDate = models.DateTimeField(default=datetime.now)
    dropDate = models.DateTimeField(blank=True, null=True)
    fare = models.FloatField(default=0.0)
    status = models.CharField(max_length=50, default="Pending")

    def __str__(self):
        return self.pickup
