#Autor: Samuel Gutierrez

from django.db import models
from django.contrib.auth.models import User
from carrito.models import Plato, Bebida  # Asegúrate de que estas importaciones son correctas
from django.conf import settings

class Orden(models.Model):
    METODO_PAGO_CHOICES = [
        ('CREDITO', 'Tarjeta de Crédito'),
        ('DEBITO', 'Tarjeta de Débito'),
    ]
    
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES)
    numero_tarjeta = models.CharField(max_length=16)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class OrdenPlato(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    
    @property
    def total(self):
        return self.cantidad * self.plato.precio

class OrdenBebida(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    bebida = models.ForeignKey(Bebida, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    
    @property
    def total(self):
        return self.cantidad * self.bebida.precio

