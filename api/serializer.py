from rest_framework import serializers
from orden.models import Orden

class OrdenSerializer(serializers.ModelSerializer):
    entregado = serializers.ReadOnlyField()

    class Meta:
        model = Orden
        fields = ['usuario', 'monto_total', 'fecha_creacion', 'entregado']