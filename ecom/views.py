from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from.forms import SignUpForm, LoginForm


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
 