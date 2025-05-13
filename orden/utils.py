#Autor: Nicolas Ruiz

from django.http import HttpRequest
from .interface import DownloadOrderInterface
import json

class DownloadProvider:
    def get_instance(self, tipo):
        if tipo == 'json':
            return DownloadOrderJson()
        elif tipo == 'txt':
            return DownloadOrderPlainText()
        else:
            raise ValueError("Tipo de descarga no soportado")

class DownloadOrderPlainText(DownloadOrderInterface):
    def download_order(self, orden, request: HttpRequest):        
        contenido = f"Orden #{orden.id}\n"
        contenido += f"Cliente: {orden.usuario.username}\n"
        contenido += f"Fecha: {orden.fecha_creacion.strftime('%Y-%m-%d %H:%M')}\n"
        contenido += f"Método de Pago: {orden.get_metodo_pago_display()}\n"
        contenido += "\nPlatos:\n"
        for item in orden.ordenplato_set.all():
            contenido += f"- {item.plato.nombre} x{item.cantidad} = ${item.total:.2f}\n"
        contenido += "\nBebidas:\n"
        for item in orden.ordenbebida_set.all():
            contenido += f"- {item.bebida.nombre} x{item.cantidad} = ${item.total:.2f}\n"
        contenido += f"\nTotal Pagado: ${orden.monto_total:.2f}\n"
        return contenido.encode('utf-8')

    def get_content_type(self):
        return 'text/plain'
    
    def get_filename(self, orden):
        return f'orden_{orden.id}.txt'
    

class DownloadOrderJson(DownloadOrderInterface):
    def download_order(self, orden, request: HttpRequest):
        data = {
            'orden_id': orden.id,
            'cliente': orden.usuario.username,
            'fecha': orden.fecha_creacion.strftime('%Y-%m-%d %H:%M'),
            'metodo_pago': orden.get_metodo_pago_display(),
            'platos': [
                {
                    'nombre': item.plato.nombre,
                    'cantidad': item.cantidad,
                    'total': str(item.total)
                } for item in orden.ordenplato_set.all()
            ],
            'bebidas': [
                {
                    'nombre': item.bebida.nombre,
                    'cantidad': item.cantidad,
                    'total': str(item.total)
                } for item in orden.ordenbebida_set.all()
            ],
            'total_pagado': str(orden.monto_total)
        }
        return json.dumps(data, indent=4).encode('utf-8')

    def get_content_type(self):
        return 'application/json'
    
    def get_filename(self, orden):
        return f'orden_{orden.id}.json'