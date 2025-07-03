#from ssl import _PasswordType
from urllib import request

from django.contrib.auth import authenticate
from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
from .models import Contact
from django.contrib import messages
from .models import Signup
from .models import Login
from django.contrib.auth.models import User
from django.contrib.auth import logout

# Create your views here.
def index(request):
    context = {
        "variable1":"Harry is great",
        "variable2":"Rohan is great"
    }
    return render(request, 'index.html', context)
    # return HttpResponse("this is homepage")

def about(request):
    return render(request, 'about.html') 

def services(request):
    return render(request, 'services.html')
 

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name=name, email=email, phone=phone, desc=desc, date = datetime.today())
        contact.save()
        messages.success(request, 'Your message has been sent!')
    return render(request, 'contact.html')

def signup(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        #desc = request.POST.get('desc')
        signup = Signup(name=name, email=email, phone=phone, password=password, date = datetime.today())
        signup.save()
        messages.success(request, 'Registration S!')
        print(name,email)
    return render(request, 'signup.html')
 
def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email='email',password='password')
        if user is not None:
            #A backend authenticated the credentials
            return redirect("/signup")
        else:
            return render(request, 'login.html')
        messages.success(request, 'Registration S!')
    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect("/login")
