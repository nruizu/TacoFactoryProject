#Autores: Samuel Gutierrez y Nicolas Ruiz

from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from .models import Orden
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from orden.utils import DownloadProvider

class DetalleOrdenView(View):
    @method_decorator(login_required)
    def get(self, request, orden_id, *args, **kwargs):
        print(f"Mostrando orden con ID: {orden_id}")
        try:
            orden = Orden.objects.get(id=orden_id, usuario=request.user)
        except Orden.DoesNotExist:
            print("Error: Orden no encontrada")
            return redirect('ver_carrito')

        return render(request, 'orden.html', {'orden': orden})
    
class DescargarOrdenView(View):
    @method_decorator(login_required)
    def get(self, request, orden_id, *args, **kwargs):
        formato = request.GET.get('formato', 'txt')
        try:
            orden = Orden.objects.get(id=orden_id, usuario=request.user)
        except Orden.DoesNotExist:
            print("Error: Orden no encontrada")
            return redirect('ver_carrito')

        tipo_descarga = DownloadProvider()
        descarga = tipo_descarga.get_instance(formato)

        contenido = descarga.download_order(orden, request)
        content_type = descarga.get_content_type()
        filename = descarga.get_filename(orden)

        # Crear respuesta HTTP con archivo descargable
        response = HttpResponse(contenido, content_type)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response