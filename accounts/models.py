from django.db import models
from django.contrib.auth.models import User
from products.models import Product



# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User , on_delete =models.CASCADE)
    
    
    product_favorites=models.ManyToManyField(Product)
    
    
    address =models.CharField(max_length=200 )
    address2 =models.CharField(max_length=200 )
    city =models.CharField(max_length=20 )
    stat =models.CharField(max_length=50 )
    zip_number =models.CharField(max_length=5)
    
    def __str__(self):
        return self.user.username

