from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from.forms import SignUpForm, LoginForm, ProductsForm
from django.shortcuts import render, get_object_or_404
from .models import Products, Payment
import uuid
from django.conf import settings
from.utils import  generate_esewa_signature
from django.views.decorators.csrf import csrf_exempt
import json, base64
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
@login_required(login_url='/login/')  # Redirects to login if not authenticated

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

 
@login_required(login_url='/login/')
def product(request):
    if request.method == 'POST':
        form = ProductsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'orders.html')
    else:
    
        form = ProductsForm()

  
    return render(request, 'ecom/product.html', {'form': form})

@login_required(login_url='/login/')
def product_list(request):
    product= Products.objects.all()
    return render(request, 'productlist.html', {'product': product})

@login_required(login_url='/login/')
def product_detail(request, pk):
    product = get_object_or_404(Products, pk=pk)
    return render(request, 'product_total.html', {'product': product})  

@login_required(login_url='/login/')        
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


    transaction_uuid = str(uuid.uuid4())  
    print("The transcation id is", transaction_uuid)
    signature = generate_esewa_signature(amount, transaction_uuid)
    print("The signature is", signature)
  
    print("The signature is", signature)

    request.session["product_id"] = product.id
    request.session["quantity"] = quantity
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


@csrf_exempt
def esewa_success(request):
    data = request.GET.get('data')

    if not data:
         return HttpResponse("Invalid response from eSewa", status=400)
    
    try:
        payload = json.loads(base64.b64decode(data).decode())
        transaction_code = payload.get("transaction_code")
        status = payload.get("status")
        total_amount = payload.get("total_amount")
        transaction_uuid = payload.get("transaction_uuid")


        # product_id = request.session.get("product_id")  

        product_id = request.session.get("product_id")
        print("The product id in success is", product_id)
        if not product_id:
            return HttpResponse("Product information missing. Cannot process payment.", status=400)

        quantity = request.session.get("quantity", 1)
        product = Products.objects.get(id=product_id)

        Payment.objects.create(
            user=request.user if request.user.is_authenticated else None,
            product=product,
            transcation_uuid=transaction_uuid,
            amount=total_amount,
            quantity=quantity,
            status=status,
        )


        
        # return HttpResponse(f"Payment Success! Transaction: {transaction_code}")
        return render(request, 'ecom/esewasuccess.html')
    except Exception as e:
        return HttpResponse(f"Error processing payment: {str(e)}", status=500)
    
@login_required(login_url='/login/')
def orderlist(request):
    user = request.user

    if user.is_staff:
        orders = Payment.objects.all()

    else:
        orders= Payment.objects.filter(user=user)

    context ={'orders': orders}

    return render(request, 'ecom/order.html', context)



 

    
 