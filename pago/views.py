from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .form import PagoForm
import datetime

# Create your views here.

class PagoView(LoginRequiredMixin, TemplateView):
    template_name = 'pago.html'
    
    def get(self, request, monto=0):
        form = PagoForm(request.POST)
        totalPago = monto
        return render(request, self.template_name, {'form': form, 'totalPago' : totalPago})
    
    def post(self, request, monto=0):
        form = PagoForm(request.POST)
        totalPago = monto
        if form.is_valid():
            form.save()
            context = {}
            context['nombre'] = self.request.user.username
            context['metodoPago'] = form.cleaned_data['metodoPago']
            context['monto'] = form.cleaned_data['monto']
            context['fecha'] = datetime.now()
            #return render(request, '../../orden/templates/orden/orden.html', data)
        else:
            return render(request, self.template_name, {'form': form, 'totalPago' : totalPago})
        
