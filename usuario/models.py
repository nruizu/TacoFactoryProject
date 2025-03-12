from django.db import models

# Create your models here.

class Usuario(models.Model):
    numDocumento = models.CharField(max_length=10, primary_key=True)
    correo = models.EmailField(max_length=50)
    celular = models.CharField(max_length=10)
    direccion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre + ' ' + self.apellido