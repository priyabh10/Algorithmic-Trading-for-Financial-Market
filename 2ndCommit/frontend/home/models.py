from django.db import models




class Contact(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    phone = models.CharField(max_length=12)
    desc = models.TextField()
    date = models.DateField()

class Signup(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    phone = models.CharField(max_length=12)
    password = models.CharField(max_length=122)
    desc = models.TextField()
    date = models.DateField()

class Login(models.Model):
    email = models.CharField(max_length=122)
    password = models.CharField(max_length=122)
    desc = models.TextField()
    date = models.DateField()

class Output(models.Model):
    pass



    def __str__(self):
        return self.name
    