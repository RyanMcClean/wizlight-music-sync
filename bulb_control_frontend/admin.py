"""Django admin file, registers the bulb module for the database"""
from django.contrib import admin
from .models import Wizbulb

# Register your models here.

admin.site.register(Wizbulb)
