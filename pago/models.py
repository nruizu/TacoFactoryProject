from django.db import models
from usuario.models import Usuario

# Create your models here.

class Pago(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    metodoPago = models.CharField(choices=[('E', 'credito'), ('T', 'debito')], max_length=1)
    numeroTarjeta = models.CharField(max_length=16)
    numeroSeguridad = models.CharField(max_length=3)
    fechaVencimiento = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.monto