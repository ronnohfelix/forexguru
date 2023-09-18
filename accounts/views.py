from django.shortcuts import render, redirect
#from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *
#from .forms import CreateUserForm
from .forms import CreateUserForm, CustomerForm
from .filters import OrderFilter
#from .decorators import unauthenticated_user, allowed_users, admin_only

#@unauthenticated_user
def registerPage(request):
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')

                group = Group.objects.get(name='customer')
                user.groups.add(group)
                Customer.objects.create(
                     user=user,
                     name=user.username,
                )
            

                messages.success(request,'Account was created for ' + username)
                return redirect('login')
        context = {'form':form}
        return render(request, 'accounts/register.html', context)

#@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
             messages.info(request, 'Username OR password is incorrect')
    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')
@login_required(login_url='login')
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST,request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'accounts/account_settings.html', context)

#@login_required(login_url='login')
#@admin_only
def home(request):
    #orders = Order.objects.all()
    #customers = Customer.objects.all()

    #total_customers = customers.count()

    #total_orders = orders.count()
    #delivered = orders.filter(status='Delivered').count()
    #pending = orders.filter(status='Pending').count()

    #context = {'orders':orders, 'customers':customers, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending}
    return render(request, 'accounts/main.html')
@login_required(login_url='login')
#@allowed_users(allowed_roles=['customer'])
def userPage(request):
    context = {}
    return render(request, 'accounts/user.html', context)



def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    context = {'customer':customer}
    return render(request, 'accounts/account_settings.html', context)