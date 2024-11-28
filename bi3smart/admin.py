from django.contrib import admin
from .models import Category, Product ,Contact,Order,Client ,ShippingAddress,OrderItem

# Register your models here.
class AdminCategory(admin.ModelAdmin):
    list_display = ('name', 'date_added')

class AdminProduct(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'date_added') 


class AdminContact(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'message','date_added')       


class AdminOrder(admin.ModelAdmin):
    list_display = ('client', 'date_orderd', 'complete', 'transactio_id')
    
class AdminClient(admin.ModelAdmin):
    list_display = ('user', 'name', 'email')

class AdminOrderItem(admin.ModelAdmin):
    list_display = ('product', 'order', 'quantity', 'date_added')    

class AdminShippingAddress(admin.ModelAdmin):
    list_display = ('client', 'order', 'address', 'city', 'zipcode', 'date_added')

admin.site.register(Product, AdminProduct)
admin.site.register(Category, AdminCategory)
admin.site.register(Contact, AdminContact)
admin.site.register(Order, AdminOrder)
admin.site.register(Client, AdminClient)
admin.site.register(ShippingAddress, AdminShippingAddress)
admin.site.register(OrderItem, AdminOrderItem)

