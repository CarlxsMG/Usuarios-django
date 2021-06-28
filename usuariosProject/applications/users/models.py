# DJango imports
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    '''Model definition for User'''

    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otros')
    )

    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=254)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=60)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)

    # Key to login in admin panel
    USERNAME_FIELD = 'username'

    def get_username(self):
        return self.username

    def get_full_name(self):
        return '{} {}'.format(self.first_name,self.last_name)