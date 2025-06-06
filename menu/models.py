from django.db import models

class Plato(models.Model):
    idPlato = models.CharField(max_length=30, primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.FloatField()
    categoria = models.CharField(max_length=20, choices=[('Combo', 'Combo'), ('Plato Fuerte', 'Plato Fuerte')])
    imagen = models.ImageField(upload_to='menu/images/')

    def __str__(self):
        return f"{self.idPlato} - {self.nombre}"
    
class Bebida(models.Model):
    idBebida = models.CharField(max_length=30, primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.FloatField()
    categoria = models.CharField(max_length=20, choices=[('Gaseosa', 'Gaseosa'), ('Agua', 'Agua')])
    cantidad = models.CharField(max_length=10, choices=[('237 ml', '237 ml'), ('280 ml', '280 ml')])
    imagen = models.ImageField(upload_to='menu/images/bebida/')

    def __str__(self):
        return f"{self.idBebida} - {self.nombre}"