from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username=None, password=None, firstName=None, lastName=None, email=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not firstName:
            raise ValueError('Users must have a first name')
        if not lastName:
            raise ValueError('Users must have a last name')
        user = self.model(email=self.normalize_email(email),firstName=firstName, lastName=lastName)

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    firstName = models.CharField(max_length=100, default='null')
    lastName = models.CharField(max_length=100, default='null')

    @property
    def getFirstName(self):
        return self.firstName

    @property
    def getLastName(self):
        return self.lastName
    objects = UserManager()