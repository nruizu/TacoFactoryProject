from django.shortcuts import render
from rest_framework import generics
from .serializer import OrdenSerializer
from orden.models import Orden

# Create your views here.

class OrdenAPI(generics.ListAPIView):
    serializer_class = OrdenSerializer

    def get_queryset(self):
        return Orden.objects.order_by('-fecha_creacion')