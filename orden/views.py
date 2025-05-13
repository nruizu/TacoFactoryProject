#Autor: Samuel Gutierrez

from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from .models import Orden
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class DetalleOrdenView(View):
    @method_decorator(login_required)
    def get(self, request, orden_id, *args, **kwargs):
        print(f"Mostrando orden con ID: {orden_id}")  # Debug
        try:
            orden = Orden.objects.get(id=orden_id, usuario=request.user)
        except Orden.DoesNotExist:
            print("Error: Orden no encontrada")  # Debug
            return redirect('ver_carrito')

        return render(request, 'orden.html', {'orden': orden})
    
class DescargarOrdenView(View):
    @method_decorator(login_required)
    def get(self, request, orden_id, *args, **kwargs):
        try:
            orden = Orden.objects.get(id=orden_id, usuario=request.user)
        except Orden.DoesNotExist:
            print("Error: Orden no encontrada")
            return redirect('ver_carrito')

        # Construir el contenido del archivo .txt
        contenido = f"Orden #{orden.id}\n"
        contenido += f"Cliente: {orden.usuario.username}\n"
        contenido += f"Fecha: {orden.fecha_creacion.strftime('%Y-%m-%d %H:%M')}\n"
        contenido += f"Método de Pago: {orden.get_metodo_pago_display()}\n"
        contenido += f"Número de Tarjeta: {orden.numero_tarjeta}\n\n"

        contenido += "Platos:\n"
        for item in orden.ordenplato_set.all():
            contenido += f"- {item.plato.nombre} x{item.cantidad} = ${item.total:.2f}\n"

        contenido += "\nBebidas:\n"
        for item in orden.ordenbebida_set.all():
            contenido += f"- {item.bebida.nombre} x{item.cantidad} = ${item.total:.2f}\n"

        contenido += f"\nTotal Pagado: ${orden.monto_total:.2f}\n"

        # Crear respuesta HTTP con archivo descargable
        response = HttpResponse(contenido, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="orden_{orden.id}.txt"'
        return response