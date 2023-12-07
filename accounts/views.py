from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse, HttpResponseRedirect
from django.forms import inlineformset_factory #to create multiple forms within one form.
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.staticfiles import finders
from django.template.loader import get_template
from django.views import View
import os, io, reportlab
from xhtml2pdf import pisa


from .models import *
from .forms import *
from .filters import *
from .decorators import *

# Create your views here.

@login_required(login_url='login') #people must be logged in to access this page. Otherwise, it'll be redirected to the login page.
@admin_only
def home(request):

    orders = Order.objects.all()
    customers = Customer.objects.all()
    out_for_delivery = orders.filter(status ='Out for delivery').count()
    delivered = orders.filter(status ='Delivered').count()
    pending = orders.filter(status ='Pending').count()
    total_orders = orders.count()

    context = {'orders':orders, 'customers':customers, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending, 'out_for_delivery':out_for_delivery}
    return render(request, 'accounts/dashboard.html', context)

@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(user=user, name=user.username)
            
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
        
    context = {'form':form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect.')
            return render(request, 'accounts/login.html')

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):

    logout(request)
    return redirect('login')

@login_required(login_url='login') #people must be logged in to access this page. Otherwise, it'll be redirected to the login page.
@allowed_users(allowed_roles=['customer','admin'])
def userPage(request):

    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status ='Delivered').count()
    pending = orders.filter(status ='Pending').count()

    print('ORDERS:', orders)

    context = {'orders':orders, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending}
    return render(request, 'accounts/user.html', context)

@login_required(login_url='login') #people must be logged in to access this page. Otherwise, it'll be redirected to the login page.
@allowed_users(allowed_roles=['admin'])
def products(request):

    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products':products})

@login_required(login_url='login') #people must be logged in to access this page. Otherwise, it'll be redirected to the login page.
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):

    customer = Customer.objects.get(id=pk)
    
    orders = customer.order_set.all()#this grabs all the orders (querying the customers child object from our model field)
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer':customer, 'orders':orders, 'order_count':order_count, 'myFilter':myFilter}
    return render(request, 'accounts/customer.html', context)

@login_required(login_url='login') #people must be logged in to access this page. Otherwise, it'll be redirected to the login page.
@allowed_users(allowed_roles=['admin'])
def createProduct(request): #This is for the admin to create a new customer.
    form = CreateProductForm()
    if request.method == 'POST':
        form = CreateProductForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/')
    return render(request, 'accounts/create_product.html', {'form':form})

@login_required(login_url='login') #people must be logged in to access this page. Otherwise, it'll be redirected to the login page.
@allowed_users(allowed_roles=['customer', 'admin'])
def accountSettingsCustomer(request): #This is for the customer to update its personal info using their own user.
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            #messages.success(request, 'Personal info is updated.')
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/account_settingsCustomer.html', context)

@login_required(login_url='login') #people must be logged in to access this page. Otherwise, it'll be redirected to the login page.
@allowed_users(allowed_roles=['admin'])
def UpdateCustomerInfo(request, pk): #This is for the customer to update its personal info using the admin user.
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            #messages.success(request, 'Personal info is updated.')
            return redirect('/')

    context = {'form':form, "customer":customer}
    return render(request, 'accounts/UpdateCustomerInfo.html', context)

@login_required(login_url='login') #people must be logged in to access this page. Otherwise, it'll be redirected to the login page.
@allowed_users(allowed_roles=['admin'])
def createOrder(request):
    form = OrderForm()
    if request.method =='POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/create_order.html', context)

""" customer = Customer.objects.get(id=pk)
    form = OrderForm(instance=customer)

    if request.method =='POST':
        form = OrderForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form, 'customer':customer}
    return render(request, 'accounts/create_order.html', context)"""



""" THIS IS A WAY OF CREATE A FORM WITH MULTIPLE LINES OF THE SAME ITEM.
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'quantity', 'status', 'note'), can_delete=False, max_num=3) #It has the parent model (Customer) and the child model (Order)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    if request.method =='POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset':formset, 'customer':customer}
    return render(request, 'accounts/order_form.html', context)
"""

@login_required(login_url='login') #people must be logged in to access this page. Otherwise, it'll be redirected to the login page.
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    
    form = OrderForm(instance=order)
    if request.method =='POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form, 'order':order}
    return render(request, 'accounts/update_order.html', context)

@login_required(login_url='login') #people must be logged in to access this page. Otherwise, it'll be redirected to the login page.
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method =='POST':
        order.delete()
        #messages.success(request, 'The order was deleted.')
        return redirect('/')

    context = {'item':order}
    return render(request, 'accounts/delete.html', context)

#____________________________________________________________________________

def render_pdf_view(request, *args, **kwargs):
    pk = kwargs.get('pk')
    customer = get_object_or_404(Customer, pk=pk)
    orders = customer.order_set.all()#this grabs all the orders (querying the customers child object from our model field)
    order_count = orders.count()

    template_path = 'accounts/pdf_template.html'
    context = {'name': customer.name,
               'phone': customer.phone,
               'email': customer.email,
               'orders': orders, 
               'order_count': order_count,
               }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #to download the pdf:
    # response['Content-Disposition'] = 'attachment; filename="CustomerInfo.pdf"'

    #to see the pdf in the browser:
    response['Content-Disposition'] = 'filename="CustomerInfo.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

    


