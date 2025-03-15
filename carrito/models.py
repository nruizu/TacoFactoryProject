from django.db import models
from menu.models import Plato, Bebida
from django.conf import settings

# Create your models here.
class Carrito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    platos = models.ManyToManyField(Plato, through='CarritoPlato')
    bebidas = models.ManyToManyField(Bebida, through='CarritoBebida')
    
    def calcular_subtotal(self):
        subtotal_platos = sum(item.plato.precio * item.cantidad for item in self.carritoplato_set.all())
        subtotal_bebidas = sum(item.bebida.precio * item.cantidad for item in self.carritobebida_set.all())
        return subtotal_platos + subtotal_bebidas
    
class CarritoPlato(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    
class CarritoBebida(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    bebida = models.ForeignKey(Bebida, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)