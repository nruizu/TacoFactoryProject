from django.contrib import admin
from .models import Plato, Bebida
# Register your models here.
from .models import Plato, Bebida

admin.site.register(Plato)
admin.site.register(Bebida)