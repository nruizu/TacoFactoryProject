#Autor: Nicolas Ruiz
from django.contrib import admin
from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('registro/', registro, name='registro'),
    path('login/', iniciar_sesion, name='login'),
    path('logout/', cerrar_sesion, name='logout'),
    path('puntos_fisicos/', views.puntos_fisicos, name='puntos_fisicos'),
]
