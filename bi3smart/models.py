from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    date_added=models.DateTimeField(auto_now=True)

    class Meta:
        ordering = [ '-date_added']
    def __str__(self) :
        return self.name   

class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category , related_name='category', on_delete=models.CASCADE)
    image = models.CharField(max_length=5000)
    date_added=models.DateTimeField(auto_now=True)
    class Meta:
        ordering = [ '-date_added']
    def __str__(self) :
        return self.title
    

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.TextField()
    message = models.TextField()
    date_added=models.DateTimeField(auto_now=True)
    class Meta:
        ordering = [ '-date_added']
    def __str__(self) :
        return self.name  



class Client(models.Model):
    user = models.OneToOneField(User ,on_delete=models.CASCADE, null=True,blank=True)  
    name = models.CharField(max_length=200 ,null=True)
    email = models. CharField(max_length=200, null=True) 
    def __str__(self):
        return self.name
    
class Order(models.Model):
    client = models.ForeignKey(Client,on_delete=models.SET_NULL ,blank=True, null=True)
    date_orderd = models.DateTimeField(auto_now_add=True)   
    complete = models.BooleanField(default=False ,null=True,blank=False)
    transactio_id = models.CharField(max_length=200 ,null=True) 
    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total() for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
     

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)   
    
    @property
    def get_total(self):
        total = self.quantity * self.product.price
        return total

class ShippingAddress(models.Model):
    client = models.ForeignKey(Client,on_delete=models.SET_NULL ,blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL ,blank=True ,null=True)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    zipcode = models.CharField(max_length=200,null=True)
    date_added = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return str(self.address)
    
class UserPurchaseHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)    







