from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from.forms import SignUpForm


def home(request):
    return render(request, 'ecom/home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user  = form.save()

            login(request, user)
            return redirect('home')
        else:
            form = SignUpForm()
            return render(request, 'ecom/signup.html', {'form': form})
        

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'ecom/login.html', {'error': 'Invalid username or password'})
        
    else:
        return render(request, 'ecom/login.html')
    
def Logout(request):
    logout(request)
    return redirect('login')
 