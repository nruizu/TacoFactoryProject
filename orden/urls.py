#Autor: Samuel Gutierrez

from django.urls import path
from .views import DetalleOrdenView

urlpatterns = [
    path('orden/<int:orden_id>/', DetalleOrdenView.as_view(), name='detalle_orden'),
]
