from django.shortcuts import render, get_object_or_404
from .models import Plato, Bebida

def menu_view(request):
    platos = Plato.objects.all()
    bebidas = Bebida.objects.all()
    return render(request, 'menu.html', {'platos': platos, 'bebidas': bebidas})

def platos_view(request):
    query = request.GET.get('q', '')
    if query:
        platos_fuertes = Plato.objects.filter(categoria='Plato Fuerte', idPlato__icontains=query)
        combos = Plato.objects.filter(categoria='Combo', idPlato__icontains=query)
    else:
        platos_fuertes = Plato.objects.filter(categoria='Plato Fuerte')
        combos = Plato.objects.filter(categoria='Combo')

    return render(request, 'platos.html', {
        'platos_fuertes': platos_fuertes,
        'combos': combos,
        'query': query
    })

def bebidas_view(request):
    query = request.GET.get('q', '')
    if query:
        aguas = Bebida.objects.filter(categoria='Agua', idBebida__icontains=query)
        gaseosas = Bebida.objects.filter(categoria='Gaseosa', idBebida__icontains=query)
    else:
        aguas = Bebida.objects.filter(categoria='Agua')
        gaseosas = Bebida.objects.filter(categoria='Gaseosa')

    return render(request, 'bebidas.html', {
        'aguas': aguas,
        'gaseosas': gaseosas,
        'query': query
    })

def buscar_plato(request, id_plato):
    plato = get_object_or_404(Plato, nombrePlato=id_plato)
    
    return render(request, 'buscar_plato.html', {
        "title": f"{plato.idPlato} - Menú",
        "subtitle": f"Detalles del plato: {plato.descripcion} - Product information",
        "plato": plato
    })

def buscar_bebida(request, id_bebida):
    bebida = get_object_or_404(Bebida, idBebida=id_bebida)
    
    return render(request, 'buscar_bebida.html', {
        "title": f"{bebida.idBebida} - Menú",
        "subtitle": f"Detalles de la bebida: {bebida.descripcion} - Product information",
        "bebida": bebida
    })