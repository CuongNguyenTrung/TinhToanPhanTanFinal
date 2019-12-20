from django.db import models

# Create your models here.

class Student(models.Model):
    mssv = models.CharField(max_length=20)
    public_key = models.CharField(max_length=100)




class Account(models.Model):
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=40)