# Autor: Camila Martínez

from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext as _
from .models import Plato, Bebida

def platos_view(request):
    query = request.GET.get('q', '').strip()
    
    if query:
        platos_fuertes = Plato.objects.filter(categoria=_('Plato Fuerte'), nombre__icontains=query)
        combos = Plato.objects.filter(categoria=_('Combo'), nombre__icontains=query)
    else:
        platos_fuertes = Plato.objects.filter(categoria=_('Plato Fuerte'))
        combos = Plato.objects.filter(categoria=_('Combo'))

    return render(request, 'platos.html', {
        'platos_fuertes': platos_fuertes,
        'combos': combos,
        'query': query
    })

def bebidas_view(request):
    query = request.GET.get('q', '').strip()
    
    if query:
        aguas = Bebida.objects.filter(categoria=_('Agua'), nombre__icontains=query)
        gaseosas = Bebida.objects.filter(categoria=_('Gaseosa'), nombre__icontains=query)
    else:
        aguas = Bebida.objects.filter(categoria=_('Agua'))
        gaseosas = Bebida.objects.filter(categoria=_('Gaseosa'))

    return render(request, 'bebidas.html', {
        'aguas': aguas,
        'gaseosas': gaseosas,
        'query': query
    })

def buscar_plato(request, nombre_plato):
    plato = get_object_or_404(Plato, nombre=nombre_plato)
    
    return render(request, 'platos.html', {
        "title": _("{name} - Menú").format(name=plato.nombre),
        "subtitle": _("Detalles del plato: {desc}").format(desc=plato.descripcion),
        "plato": plato
    })

def buscar_bebida(request, nombre_bebida):
    bebida = get_object_or_404(Bebida, nombre=nombre_bebida)
    
    return render(request, 'bebidas.html', {
        "title": _("{name} - Menú").format(name=bebida.nombre),
        "subtitle": _("Detalles de la bebida: {desc}").format(desc=bebida.descripcion),
        "bebida": bebida
    })