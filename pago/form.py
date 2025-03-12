from .models import Pago
from django import forms

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = '__all__'