#Autor: Samuel Gutierrez

from django.urls import path
from .views import DetalleOrdenView, DescargarOrdenView

urlpatterns = [
    path('orden/<int:orden_id>/', DetalleOrdenView.as_view(), name='detalle_orden'),
    path('orden/<int:orden_id>/descargar/', DescargarOrdenView.as_view(), name='descargar_orden'),
]
