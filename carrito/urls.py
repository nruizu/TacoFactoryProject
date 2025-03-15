from django.urls import path
from . import views

urlpatterns = [
    path('', views.ver_carrito, name='ver_carrito'),
    path('agregar/<str:tipo>/<str:item_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('actualizar/<str:tipo>/<str:item_id>/' )
]