from django.shortcuts import render, get_object_or_404
from .models import Plato, Bebida

def platos_view(request):
    query = request.GET.get('q', '').strip()
    
    if query:
        platos_fuertes = Plato.objects.filter(categoria='Plato Fuerte', nombre__icontains=query)
        combos = Plato.objects.filter(categoria='Combo', nombre__icontains=query)
    else:
        platos_fuertes = Plato.objects.filter(categoria='Plato Fuerte')
        combos = Plato.objects.filter(categoria='Combo')

    return render(request, 'platos.html', {
        'platos_fuertes': platos_fuertes,
        'combos': combos,
        'query': query
    })

def bebidas_view(request):
    query = request.GET.get('q', '').strip()
    
    if query:
        aguas = Bebida.objects.filter(categoria='Agua', nombre__icontains=query)
        gaseosas = Bebida.objects.filter(categoria='Gaseosa', nombre__icontains=query)
    else:
        aguas = Bebida.objects.filter(categoria='Agua')
        gaseosas = Bebida.objects.filter(categoria='Gaseosa')

    return render(request, 'bebidas.html', {
        'aguas': aguas,
        'gaseosas': gaseosas,
        'query': query
    })

def buscar_plato(request, nombre_plato):
    plato = get_object_or_404(Plato, nombre=nombre_plato)
    
    return render(request, 'platos.html', {
        "title": f"{plato.nombre} - Menú",
        "subtitle": f"Detalles del plato: {plato.descripcion}",
        "plato": plato
    })

def buscar_bebida(request, nombre_bebida):
    bebida = get_object_or_404(Bebida, nombre=nombre_bebida)
    
    return render(request, 'bebidas.html', {
        "title": f"{bebida.nombre} - Menú",
        "subtitle": f"Detalles de la bebida: {bebida.descripcion}",
        "bebida": bebida
    })