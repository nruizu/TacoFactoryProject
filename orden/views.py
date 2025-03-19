from django.shortcuts import render, redirect
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

        return render(request, 'orden.html', {'orden': orden})  # 🔴 Ruta corregida
