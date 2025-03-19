from .models import Pago
from django import forms

class PagoForm(forms.ModelForm):
    metodoPago = forms.ChoiceField(choices=Pago.METODOS_PAGO, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Pago
        fields = ['metodoPago', 'numeroTarjeta', 'numeroSeguridad', 'fechaVencimiento']
