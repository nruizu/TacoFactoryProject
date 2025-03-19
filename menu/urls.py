#Autor: Camila Martínez

from django.urls import path
from .views import platos_view, bebidas_view, buscar_plato, buscar_bebida

urlpatterns = [
    path('platos/', platos_view, name='platos'),
    path('bebidas/', bebidas_view, name='bebidas'),
    path('platos/<str:idPlato>/', buscar_plato, name='buscar_plato'),
    path('bebidas/<str:idBebida>/', buscar_bebida, name='buscar_bebida'),
] 
