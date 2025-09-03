from django.db import models



class Products(models.Model):
    name = models.CharField(max_length = 100)
    photo = models.ImageField(upload_to='products/')  
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    description= models.TextField(blank=True)
    quantity= models.IntegerField(default=0)

    def __str__(self):
        return self.name

