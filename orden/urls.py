from django.urls import path
from .views import CrearOrdenView, DetalleOrdenView

urlpatterns = [
    path('detalle/<int:orden_id>/', DetalleOrdenView.as_view(), name='detalle_orden'),
]
