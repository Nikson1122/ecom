from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone




class Products(models.Model):
    name = models.CharField(max_length = 100)
    photo = models.ImageField(upload_to='products/')  
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    description= models.TextField(blank=True)
    quantity= models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class Payment(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
     product = models.ForeignKey(Products, on_delete=models.CASCADE)
     transcation_uuid = models.CharField(max_length=100)
     amount = models.DecimalField(max_digits=10, decimal_places=2)
     quantity = models.PositiveIntegerField(default=1)
     status = models.CharField(max_length=20)
     created_at = models.DateTimeField(default=timezone.now)

def __str__(self):
    return f"{self.product}-{self.transcation_uuid}"
         



