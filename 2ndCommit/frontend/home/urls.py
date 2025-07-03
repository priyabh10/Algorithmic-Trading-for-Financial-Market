from django.contrib import admin
from django.urls import path
from home import views
from home.models import Login


urlpatterns = [
    path("", views.index, name='home'),
    path("about", views.about, name='about'),
    path("services", views.services, name='services'),
    path("contact", views.contact, name='contact'), 
    path("signup",views.signup,name='signup'),
    path("login",views.login,name='login'),
    #path('output',views.output,name='script'),
    path('output',views.output,name='script')
]