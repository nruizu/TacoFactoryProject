#Autor: Nicolas Ruiz
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('pago/', PagoView.as_view(), name='pago'),
]
