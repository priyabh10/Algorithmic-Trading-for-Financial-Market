#from ssl import _PasswordType
from urllib import request
from django.shortcuts import render, HttpResponse
from datetime import datetime
from home.models import Contact
from django.contrib import messages
from home.models import Signup
from home.models import Login

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

def Signup(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.Post.get('password')
        desc = request.POST.get('desc')
        Signup = Contact(name=name, email=email, phone=phone, password=password, desc=desc, date = datetime.today())
        Signup.save()
        messages.success(request, 'Registration S!')
    return render(request, 'signup.html')
 
def Login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.Post.get('password')
        desc = request.POST.get('desc')
        Login = Contact( email=email, password=password, desc=desc, date = datetime.today())
        Login.save()
        messages.success(request, 'Registration S!')
    return render(request, 'login.html')