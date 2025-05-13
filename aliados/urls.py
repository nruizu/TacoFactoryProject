from django.urls import path
from .views import productos_aliados, detalle_curso

urlpatterns = [
    path('', productos_aliados, name='productos_aliados'),
    path('<int:id>/', detalle_curso, name='detalle_curso'),
]
