#Autor: Nicolas Ruiz
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Usuario(AbstractUser):
    email = models.EmailField(max_length=50, unique=True)
    numDocumento = models.CharField(max_length=10, unique=True)
    celular = models.CharField(max_length=10)
    direccion = models.CharField(max_length=100)

    # Definir el correo como el campo de login principal
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["numDocumento", "username"]

    def __str__(self):
        return self.email