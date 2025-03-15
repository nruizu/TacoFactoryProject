from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Carrito, CarritoPlato, CarritoBebida, Plato, Bebida

# Create your views here.
@login_required
def ver_carrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    platos = CarritoPlato.objects.filter(carrito=carrito)
    bebidas = CarritoBebida.objects.filter(carrito=carrito)
    
    context = {
        'carrito': carrito,
        'platos': platos,
        'bebidas': bebidas
    }
    return render(request, 'carrito/ver_carrito.html', context)

@login_required
def agregar_al_carrito(request, tipo, item_id):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    
    if tipo == "plato":
        plato = get_object_or_404(Plato, idPlato=item_id)
        carrito_item, created = CarritoPlato.objects.get_or_create(carrito=carrito, plato=plato)
        carrito_item.cantidad += 1
        carrito_item.save()
        
    elif tipo == "bebida":
        bebida = get_object_or_404(Bebida, idBebida=item_id)
        carrito_item, created = CarritoBebida.objects.get_or_create(carrito=carrito, bebida=bebida)
        carrito_item.cantidad += 1
        carrito_item.save()
        
    return redirect('ver_carrito')

@login_required
def eliminar_del_carrito(request, tipo, item_id):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    
    if tipo == "plato":
        CarritoPlato.objects.filter(carrito=carrito, plato_id=item_id).delete()
        
    elif tipo == "bebida":
        CarritoBebida.objects.filter(carrito=carrito, bebida_id=item_id).delete()
        
    return redirect('ver_carrito')

@login_required
def actualizar_cantidad(request, tipo, item_id, cantidad):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    
    if tipo == "plato":
        item = get_object_or_404(CarritoPlato, carrito=carrito, plato_id=item_id)
    elif tipo == "bebida":
        item = get_object_or_404(CarritoBebida, carrito=carrito, bebida_id=item_id)
        
    item.cantidad = max(1, cantidad)
    item.save()
    
    return redirect('ver_carrito')

@login_required
def vaciar_carrito(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    CarritoPlato.objects.filter(carrito=carrito).delete()
    CarritoBebida.objects.filter(carrito=carrito).delete()
    
    return redirect('ver_carrito')