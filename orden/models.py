from django.db import models
from django.contrib.auth.models import User
from carrito.models import Plato, Bebida  # Asegúrate de que estas importaciones son correctas
from django.conf import settings

class Orden(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50)
    numero_tarjeta = models.CharField(max_length=16)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class OrdenPlato(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

class OrdenBebida(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    bebida = models.ForeignKey(Bebida, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

