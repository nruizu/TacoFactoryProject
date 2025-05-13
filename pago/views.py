#Autor: Nicolas Ruiz
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, reverse
from .form import PagoForm
from orden.models import Orden, OrdenPlato, OrdenBebida
from carrito.models import Carrito, CarritoPlato, CarritoBebida

class PagoView(LoginRequiredMixin, TemplateView):
    template_name = 'pago.html'

    def get(self, request, *args, **kwargs):
        monto = request.session.get('monto', 0)

        if monto <= 0:
            return redirect('ver_carrito')

        form = PagoForm()
        return render(request, self.template_name, {'form': form, 'totalPago': monto})

    def post(self, request, *args, **kwargs):
        print("📢 Datos recibidos en POST:", request.POST)
        monto = request.session.get('monto', 0)
        form = PagoForm(request.POST)

        if form.is_valid():
            pago = form.save(commit=False)
            pago.monto = monto
            pago.usuario = request.user
            pago.save()                     

            print("✅ Pago exitoso")
            usuario = request.user
            metodo_pago = form.cleaned_data['metodoPago']
            numero_tarjeta = form.cleaned_data['numeroTarjeta']

            # Obtener el carrito del usuario
            try:
                carrito = Carrito.objects.get(usuario=usuario)
            except Carrito.DoesNotExist:
                print("Error: Carrito no encontrado")  # Debug
                return redirect('ver_carrito')

            # Crear la orden
            orden = Orden.objects.create(
                usuario=usuario,
                monto_total=monto,
                metodo_pago=metodo_pago,
                numero_tarjeta=numero_tarjeta
            )

            # Agregar los platos del carrito a la orden
            for item in CarritoPlato.objects.filter(carrito=carrito):
                OrdenPlato.objects.create(
                    orden=orden,
                    plato=item.plato,
                    cantidad=item.cantidad
                )

            # Agregar las bebidas del carrito a la orden
            for item in CarritoBebida.objects.filter(carrito=carrito):
                OrdenBebida.objects.create(
                    orden=orden,
                    bebida=item.bebida,
                    cantidad=item.cantidad
                )

            # Vaciar el carrito después de la compra
            carrito.platos.clear()
            carrito.bebidas.clear()

            # Redirigir a la vista de detalle de la orden
            return redirect(reverse('detalle_orden', kwargs={'orden_id': orden.id}))
    
        else:
            print("❌ Error en el formulario:", form.errors)
        return render(request, self.template_name, {'form': form, 'totalPago': monto})