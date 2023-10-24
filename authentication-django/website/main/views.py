from django.shortcuts import render, redirect
from main.forms import RegisterForm
from django.contrib.auth import login, logout, authenticate

# Create your views here.

def home(request):
    return render(request, 'main/home.html')

def sign_up(request):
    print('request keldi pastda')
    print(request)
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()
    print(form)
        
    return render(request, 'registration/sign_up.html', {"form":form})

