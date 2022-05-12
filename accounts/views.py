from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .forms import CustomerCreateForm, OrderCreateForm, ProductCreateForm,CreateUserForm
from .models import *
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, only_admin


# Create your views here.

def register(request):
    # if request.user.is_authenticated:
    #     return redirect('main')
    # else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user=form.save()
                username= form.cleaned_data.get('username')
                group = Group.objects.get(name='customer')
                user.groups.add(group)
                Customer.objects.create(
                    user=user,
                    name=user.username
                )
                messages.success(request,'Account created for' + username)
                return redirect('login')
        context={ 'form': form }
        return render(request,'accounts/register.html',context)

@unauthenticated_user
def loginpage(request):
    # if request.user.is_authenticated:
    #     return redirect('main')
    # else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('main')

        context= {}
        return render(request, 'accounts/login.html', context)

def logoutpage(request):
    logout(request)
    return redirect('main')

@login_required(login_url='login')
@only_admin
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    order_delivered = orders.filter(status='Delivered').count()
    order_pending = orders.filter(status='Pending').count()
    context = {
        'orders': orders,
        'customers':customers,
        'total_customers':total_customers,
        'total_orders':total_orders,
        'order_delivered':order_delivered,
        'order_pending':order_pending
    }
    return render(request,'accounts/dashboard.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customers(request,pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    total_orders = orders.count()
    myFilter = OrderFilter(request.GET,queryset=orders)
    orders = myFilter.qs
    context = {
        'customer':customer,
        'orders':orders,
        'total_orders':total_orders,
        'myFilter':myFilter
    }
    return render(request,'accounts/customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()

    context = {
        'products': products
    }
    return render(request,'accounts/product.html' , context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createcustomer(request):
    form = CustomerCreateForm()
    context={
        'form':form
    }
    if request.method=='POST':
        form = CustomerCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('main')
    return render(request, 'accounts/create_customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createorder(request):
    form = OrderCreateForm()
    context={
        'form':form
    }
    if request.method=='POST':
        form = OrderCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('main')
    return render(request, 'accounts/create_order.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createproduct(request):
    form = ProductCreateForm()
    context={
        'form':form
    }
    if request.method=='POST':
        form = ProductCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('products')
    return render(request, 'accounts/create_order.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateorder(request,pk):
    order=Order.objects.get(id=pk)
    form = OrderCreateForm(instance=order)
    context = {
        'form': form
    }
    if request.method=='POST':
        form = OrderCreateForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('main')
    return render(request,'accounts/create_order.html',context)

@allowed_users(allowed_roles=['admin'])
def deleteorder(request,pk):
    order = Order.objects.get(id=pk)
    context = {
        'order':order
    }

    if request.method=='POST':
        order.delete()
        return redirect('main')
    return render(request, 'accounts/delete_order.html',context)

@allowed_users(allowed_roles=['admin'])
def updatecustomer(request,pk):
    customer=Customer.objects.get(id=pk)
    form = CustomerCreateForm(instance=customer)
    context = {
        'form': form
    }
    if request.method=='POST':
        form = CustomerCreateForm(request.POST,instance=customer)
        if form.is_valid():
            form.save()
            return redirect('main')
    return render(request,'accounts/create_customer.html',context)

@allowed_users(allowed_roles=['admin'])
def deletecustomer(request,pk):
    customer = Customer.objects.get(id=pk)
    context = {
        'customer':customer
    }

    if request.method=='POST':
        customer.delete()
        return redirect('main')
    return render(request, 'accounts/delete_customer.html',context)

@allowed_users(allowed_roles=['admin'])
def createorderscustomer(request, pk):
    OrderFormSet = inlineformset_factory(Customer , Order , fields=('product' , 'status'),extra=10)
    customer= Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none() ,instance=customer)
    #form = OrderCreateForm(initial={'customer':customer})

    if request.method=='POST':
        formset = OrderFormSet(request.POST , instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('main')
    context = {
        'formset': formset
    }
    return render(request, 'accounts/create_order_formset.html', context)

@allowed_users(allowed_roles=['customer'])
def userspage(request):

    orders= request.user.customer.order_set.all()
    total_orders = orders.count()
    order_delivered = orders.filter(status='Delivered').count()
    order_pending = orders.filter(status='Pending').count()
    context = {'orders':orders,
               'total_orders':total_orders,
               'order_delivered':order_delivered,
               'order_pending':order_pending
               }
    return render(request,'accounts/users.html',context)

def profilepage(request):
    context={}
    return render(request, 'accounts/profile.html', context)

def edit_profile(request):
    form = CustomerCreateForm(instance=request.user.customer)
    if request.method == 'POST':
        form=CustomerCreateForm(request.POST,request.FILES, instance=request.user.customer)
        if form.is_valid():
            form.save()
            return redirect('profile')
    context={'form':form }
    return render(request, 'accounts/edit_profile.html', context)
