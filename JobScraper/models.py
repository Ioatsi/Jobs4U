from django.db import models
from flask import session
from django.contrib.sessions.models import Session
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django import forms
# Create your models here.
class SearchSession(models.Model):
    searchTerm = models.CharField(max_length=200)
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, blank=False, null=True)
    title=models.CharField(max_length=200)
class UserManager(BaseUserManager):
    def create_user(self, username=None, password=None, firstName=None, lastName=None, email=None):
        user = self.model(username=username,email=email,first_name=firstName, last_name=lastName)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    
    @property
    def getFirstName(self):
        return self.first_name

    @property
    def getLastName(self):
        return self.last_name

    @property
    def getPass(self):
        return self.password

    objects = UserManager()

class JobListing(models.Model):
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    source = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    details = models.CharField(max_length=500)
    

class Saved(models.Model):
    JobListing = models.ForeignKey(JobListing,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE, default=1)

class History(models.Model):
    JobListing = models.ForeignKey(JobListing,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE, default=1)
    
class Lists(models.Model):
    listName= models.CharField(max_length=200)
    user = models.ForeignKey(User,on_delete=models.CASCADE, default=1)
    
class CustomListings(models.Model):
    listName = models.ForeignKey(Lists,on_delete=models.CASCADE)
    JobListing = models.ForeignKey(JobListing,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE, default=1)

