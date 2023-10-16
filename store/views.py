from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from .utils import  cartData
from django.contrib import auth

from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import   ProductForm, UserRegisterForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from .models import * 

#Create your views here.

def store(request):
    customer = None  # Initialize as None
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']
        
    products = Product.objects.all()
    
    if request.user.is_authenticated:
        custm = Customer.objects.get(user=request.user)
        context = {'products': products, 'cartItems': cartItems, "customer": custm.role}
    else:
        context = {'products': products, 'cartItems': cartItems, "customer": None}
    
    return render(request, 'store/store.html', context)


def product_view(request, myid):
    product = Product.objects.filter(id=myid).first()
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']
 
    return render(request, 'store/product_view.html', {'product':product, 'cartItems':cartItems})

def cart(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
      
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']
        
    context = {'items':items,  'order':order, 'cartItems':cartItems}
    return render(request,  'store/cart.html', context)


def checkout(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']
        
    context = {'items':items,  'order':order, 'cartItems':cartItems}
    return render(request,  'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    print('Action:', action)
    print('Product:', productId)
    
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        
        if total == order.get_cart_total:
            order.complete = True
        order.save()
        
        if order.shipping == True:
            ShippingAddress.objects.create(
                cu=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
        
    else:
        print('User is not logged in..')
    return JsonResponse('Payment complete!', safe=False)

  
########### register here #####################################

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) or None
        if form.is_valid():
            username = request.POST.get('username')
            
         
            #########################mail####################################
            # htmly = get_template('store/Email.html')
            # d = { 'username': username }
            # subject, from_email, to = 'hello', 'from@example.com', 'to@emaple.com'
            # html_content = htmly.render(d)
            # msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            # msg.attach_alternative(html_content, "text/html")
            # try:
            #     msg.send()
            # except:
            #     print("error in sending mail")
            ##################################################################
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            role = request.POST.get('farmer')
            us = User.objects.get(username=username)
            Customer.objects.create(name=username,email=email,role=role,user=us)
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'store/register.html', {'form': form,'title':'reqister here'})





  
################ login forms###################################################
def Login(request):
    if request.method == 'POST':
  
        # AuthenticationForm_can_also_be_used__
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            form = login(request,user)
            messages.success(request, f' wecome {username} !!')
            return redirect('store')
        
        if hasattr(user, 'farmer'):
                    return redirect('add_products')

        else:
            messages.info(request, f'account done not exit plz sign in')
    form = AuthenticationForm()
    return render(request, 'store/login.html', {'form':form, 'title':'log in'})


def farmer_profile(request):
    return render(request, 'add_product/farmer_profile.html', {})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('store')  # Redirect to a view that displays all products
    else:
        form = ProductForm()
        print(form)

    return render(request, 'store/add_product.html', {'form': form})

def logout(request):
    auth.logout(request)
    return redirect('login')