# Editado por Samuel Gutierrez

"""
URL configuration for taco_factory project.
The `urlpatterns` list routes URLs to views.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    # Ruta para cambiar el idioma
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('pago.urls')),
    path('', include('usuario.urls')),
    path('', include('menu.urls')),
    path('carrito/', include('carrito.urls')),
    path('orden/', include('orden.urls')),
    path('api/', include('api.urls')),
    path('productos-aliados/', include('aliados.urls')),
    prefix_default_language=False  
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)