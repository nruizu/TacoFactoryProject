#Autor: Camila Martínez

from django.db import models

class Plato(models.Model):
    idPlato = models.CharField(max_length=30, primary_key= True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.FloatField()
    categoria = models.CharField(max_length=20, choices=[('Combo', 'Combo'), ('Plato Fuerte', 'Plato Fuerte')])
    imagen = models.ImageField(upload_to='plato/', blank=True, null=True)

    def __str__(self):
        return self.idPlato, self.nombre
    
class Bebida(models.Model):
    idBebida = models.CharField(max_length=30, primary_key= True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.FloatField()
    categoria = models.CharField(max_length=20, choices=[('Gaseosa', 'Gaseosa'), ('Agua', 'Agua')])
    cantidad = models.CharField(max_length=10, choices=[('237 ml', '237 ml'), ('280 ml', '280 ml')])
    imagen = models.ImageField(upload_to='bebida/', blank=True, null=True)

    def __str__(self):
        return self.idBebida, self.nombre
