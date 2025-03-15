from django.contrib import admin
from .models import Carrito

# Register your models here.
@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'subtotal')
    
    def subtotal(self, obj):
        return obj.calcular_subtotal()
    subtotal.short_description = 'Subtotal'