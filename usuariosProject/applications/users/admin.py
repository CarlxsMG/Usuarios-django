# DJango imports
from django.contrib import admin

# Local models
from .models import User

# Register your models here.
admin.site.register(User)