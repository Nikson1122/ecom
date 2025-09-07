from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from.forms import SignUpForm, LoginForm, ProductsForm
from django.shortcuts import render, get_object_or_404
from .models import Products
import uuid
from django.conf import settings
from.utils import  generate_esewa_signature
from django.views.decorators.csrf import csrf_exempt



def home(request):
    return render(request, 'ecom/base.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    
    return render(request, 'ecom/Signup.html', {'form': form})

def Login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                # Add non-field error to the form
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'ecom/login.html', {'form': form})
    
def Logout(request):
    logout(request)
    return redirect('login')

 

def product(request):
    if request.method == 'POST':
        form = ProductsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'orders.html')
    else:
    
        form = ProductsForm()

  
    return render(request, 'ecom/product.html', {'form': form})

def product_list(request):
    product= Products.objects.all()
    return render(request, 'productlist.html', {'product': product})

def product_detail(request, pk):
    product = get_object_or_404(Products, pk=pk)
    return render(request, 'product_total.html', {'product': product})  
        
def orders(request):
        return render(request, 'orders.html')



@csrf_exempt
def initiate_payment(request, product_id):
    product = Products.objects.get(id=product_id)
    name = product
    print("The product name is", name)
    amount = request.POST.get("total_amount") 
    quantity = request.POST.get("quantity")
    print("The quantity is", quantity)
    
    print("The amount is" , amount)
    print("POST data:", request.POST)


    transaction_uuid = str(uuid.uuid4())  # fixed spelling
    print("The transcation id is", transaction_uuid)
    signature = generate_esewa_signature(amount, transaction_uuid)
    print("The signature is", signature)
  
    print("The signature is", signature)
    success_url = request.build_absolute_uri('/esewa/success/')
    failure_url = request.build_absolute_uri('/esewa/failure/')
  
    context = {
        'product': product,
        'transaction_uuid': transaction_uuid,  # fixed
        'product_code': settings.ESEWA_MERCHANT_ID,  # if you want to send merchant id as product code
        'amount': amount,
        'total_amount': amount,  # assuming no extra charges
        'tax_amount': 0,  # default tax if not used
        'product_service_charge': 0,
        'product_delivery_charge': 0,
        'signature': signature,
        'success_url': success_url,
        'failure_url': failure_url,
        'signed_field_names': 'total_amount,transaction_uuid,product_code',
        'signature': signature,
    }

    return render(request, 'esewa.html', context)




 

    
 