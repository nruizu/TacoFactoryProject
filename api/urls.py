#Autor: Nicolas Ruiz
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', OrdenAPI.as_view(), name='api'),
]
