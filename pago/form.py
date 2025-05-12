#Autor: Nicolas Ruiz
from .models import Pago
from django import forms

class PagoForm(forms.ModelForm):
    metodoPago = forms.ChoiceField(
        choices=Pago.METODOS_PAGO,
        label="Método de pago",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    numeroTarjeta = forms.CharField(
        label="Número de Tarjeta",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    numeroSeguridad = forms.CharField(
        label="Número de Seguridad",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    fechaVencimiento = forms.DateField(
        label="Fecha de Vencimiento",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Pago
        fields = ['metodoPago', 'numeroTarjeta', 'numeroSeguridad', 'fechaVencimiento']
