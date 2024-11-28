from django import forms
from .models import Product,Contact,Order

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'image', 'price','category']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']     

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'



      
