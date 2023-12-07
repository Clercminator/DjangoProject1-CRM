from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User

# Create your models here.

class Customer(Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE) #CASCADE means that whenever an user is deleted, the relationship to that customer will be deleted as well. A OneToOne field means that an user can have one customer and a customer can only have one user.
    name = models.CharField(max_length=200, null=True)
    phone = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name
    
class Tag(Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
    
class Product(Model):
    CATEGORY = (
                ('Indoor','Indoor'),
                ('Outdoor','Outdoor'),
                ('Mixed','Mixed'),
            )
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name
    
class Order(Model):
    customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
    quantity = models.IntegerField(null=True)
    STATUS = (
                ('Pending','Pending'),
                ('Out for delivery','Out for delivery'),
                ('Delivered','Delivered'),
            )
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    note = models.CharField(max_length=1000, null=True, blank=True)
    
    def __str__(self):
        return self.product.name
    