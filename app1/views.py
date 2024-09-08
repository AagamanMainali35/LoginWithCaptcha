import re
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests


# Create your views here.

@login_required(login_url='login')
def HomePage(request):
     return render(request, 'home.html')

def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('confirm_password')
        special_characters = re.compile('[@_!#$%^&*()<>?/\\|}{~:]')
        check=User.objects.filter(username=uname)
        print(check)
        if pass1 != pass2:
            messages.error(request,"Different passwords detected")
        elif not special_characters.search(pass1):
            messages.error(request," Please  Include special character")
        elif check.exists():
            messages.error(request,'The username already exists.Try Again  ! ')
        else:
            my_user = User.objects.create_user(username=uname, password=pass1)
            my_user.save()
            return redirect('login')
    return render(request, 'register.html')
    


def LoginPage(request):
    if request.method=='POST':
        recaptcha_response = request.POST.get('g-recaptcha-response')
        secret_key = '6LcCezYqAAAAAJd7Dgjl8PJpW2xjg3sOw1gDNymw'
        payload = {
            'secret': secret_key,
            'response': recaptcha_response
        }
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
        result = response.json()
        if result.get('success'):
            Loginusername=request.POST.get('Lusername')
            pwd=request.POST.get('Lpassword')
            user=authenticate(request,username=Loginusername,password=pwd)
            if user is not None:
                login(request,user)  
                return redirect('home') 
            else:
                messages.error(request,'password didnt match')
    return render(request,'login.html') 

def Logoutpage(request):
     logout(request)
     return redirect('login')
