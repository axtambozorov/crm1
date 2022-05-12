from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE,blank=True)
    name = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=13,null=True)
    email = models.CharField(max_length=25,null=True)
    profile_pic = models.ImageField(null=True,blank=True,default='picture.png')
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.name

class Tags(models.Model):
    name = models.CharField(max_length=200,null=True,verbose_name='Tag')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Tag'

class Product(models.Model):
    CATEGORY=(
        ('Indoor' , 'Indoor'),
        ('Out door' , 'Out door'),
    )
    name=models.CharField(max_length=200,null=True)
    price=models.FloatField(null=True)
    category=models.CharField(max_length=200,null=True, choices=CATEGORY)
    description =models.TextField(blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    tags=models.ManyToManyField(Tags)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS=(
        ('Pending' , 'Pending'),
        ('Out for delevery' , 'Out for delevery'),
        ('Delivered' , 'Delivered'),
    )
    customer=models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
    product=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    status=models.CharField(max_length=200,null=True,choices=STATUS)

    def __str__(self):
        return self.status