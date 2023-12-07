#Model form: It's a python way to build out our forms, add them into a template and process and save that data.
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from .models import *

class CustomerForm(ModelForm):#form to create a new order and for the customer to be able to update its info.
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']

class OrderForm(ModelForm): #form to create a new order.
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {'customer': forms.Select(attrs={'class': 'form-control'}),
                   'product': forms.Select(attrs={'class': 'form-control'}),
                   'quantity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write it in numbers.', 'type':'number'}),
                   'status': forms.Select(attrs={'class': 'form-control'}),
                   'note': forms.TextInput(attrs={'class': 'form-control'}),}

class CreateUserForm(UserCreationForm): #form to create a new user in the register page.
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CreateProductForm(ModelForm): #form to create a new user in the register page.
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'description', 'tags']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}),
                   'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write it in numbers.', 'type':'number'}),
                   'category': forms.Select(attrs={'class': 'form-control'}),
                   'description': forms.TextInput(attrs={'class': 'form-control'}),
                   'tags': forms.CheckboxSelectMultiple(attrs={'class': 'form-control d-flex justify-content-around'}),}
