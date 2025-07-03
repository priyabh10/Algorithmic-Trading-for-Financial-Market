
from multiprocessing import context
import re
from urllib import request
from django.shortcuts import render
from datetime import datetime
from home import orb_stat
from home.models import Contact
from django.contrib import messages
from home.models import Signup
from home.models import Login
from home import document_file
from home import views
from home import orb_stat
from django.http import HttpResponse


def index(request):
    context = {
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
        desc = request.POST.get('desc')
        signup = Signup(name=name, email=email, phone=phone, password=password, desc=desc, date = datetime.today())
        signup.save()
        messages.success(request, 'Registration S!')
    return render(request, 'signup.html')
 
def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        desc = request.POST.get('desc')
        login = Login( email=email, password=password, desc=desc, date = datetime.today())
        login.save()
        messages.success(request, 'Registration S!')
    return render(request, 'login.html')

def output(request):
    if request.method == 'POST':
        print("i am inside if")
        auth_code = request.POST.get('auth')
        print(auth_code)   
        data=orb_stat.main(auth_code)
        print(data)
        return render(request, 'trading_window.html',{'data':data})
    
    else :
        
        context ={
            'auth_code_url':  orb_stat.generate_auth_code()
        }
        return render(request, 'auth_code.html', context)





    
