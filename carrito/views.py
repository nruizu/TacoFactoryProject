#Autor: Samuel Gutierrez

import json
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from .models import Carrito, CarritoPlato, CarritoBebida, Plato, Bebida
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@login_required
def ver_carrito(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    platos = CarritoPlato.objects.filter(carrito=carrito)
    bebidas = CarritoBebida.objects.filter(carrito=carrito)

    # Calcular el subtotal
    subtotal = sum(item.plato.precio * item.cantidad for item in platos) + \
               sum(item.bebida.precio * item.cantidad for item in bebidas)

    # Guardar el subtotal en la sesión
    request.session['monto'] = subtotal

    context = {
        'carrito': carrito,
        'platos': platos,
        'bebidas': bebidas,
        'subtotal': subtotal,  # Pasar subtotal al template
    }

    return render(request, 'carrito.html', context)

@csrf_exempt
def agregar_al_carrito(request):
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "redirect": "/login/?next=" + request.path}, status=401)

    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

    try:
        data = json.loads(request.body.decode('utf-8'))  # Intentar obtener JSON
        tipo = data.get("tipo")
        item_id = data.get("item_id")
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "message": "Error en formato JSON"}, status=400)

    if not tipo or not item_id:
        return JsonResponse({"success": False, "message": "Datos incompletos"}, status=400)

    if tipo == "plato":
        plato = get_object_or_404(Plato, idPlato=item_id)
        carrito_item, created = CarritoPlato.objects.get_or_create(carrito=carrito, plato=plato)
    elif tipo == "bebida":
        bebida = get_object_or_404(Bebida, idBebida=item_id)
        carrito_item, created = CarritoBebida.objects.get_or_create(carrito=carrito, bebida=bebida)
    else:
        return JsonResponse({"success": False, "message": "Tipo de producto inválido"}, status=400)

    if created:
        carrito_item.cantidad = 1
    else:
        carrito_item.cantidad += 1
    carrito_item.save()

    return JsonResponse({"success": True, "message": "Producto agregado al carrito", "cantidad": carrito_item.cantidad})

@login_required
def eliminar_del_carrito(request, tipo, item_id):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    
    if tipo == "plato":
        item = get_object_or_404(CarritoPlato, carrito=carrito, id=item_id)
        
    elif tipo == "bebida":
        item = get_object_or_404(CarritoBebida, carrito=carrito, id=item_id)
        
    item.delete()
    return JsonResponse({"success": True, "message": "Producto eliminado del carrito"})

@login_required
@csrf_exempt
def actualizar_cantidad(request):
    if request.method == "POST":
        tipo = request.POST.get('tipo')
        item_id = request.POST.get('item_id')
        cantidad = int(request.POST.get('cantidad', 1))
        
        carrito = get_object_or_404(Carrito, usuario=request.user)
    
        if tipo == "plato":
            item = get_object_or_404(CarritoPlato, carrito=carrito, id=item_id)
        elif tipo == "bebida":
            item = get_object_or_404(CarritoBebida, carrito=carrito, id=item_id)
        else:
            return JsonResponse({'error': 'Tipo invalido'})
        
        item.cantidad = max(1, cantidad)
        item.save()
        
        return JsonResponse({"success": True, "nueva cantidad": item.cantidad})
    
    return JsonResponse({'error': 'Metodo no permitido'}, status=405)

@login_required
def vaciar_carrito(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    CarritoPlato.objects.filter(carrito=carrito).delete()
    CarritoBebida.objects.filter(carrito=carrito).delete()
    
    return redirect('ver_carrito')

@login_required
def proceder_pago(request):
    monto = request.session.get('monto', 0)  # Obtener el monto de la sesión
    
    if monto <= 0:
        return redirect('ver_carrito')  # Evitar pagos sin monto válido

    return redirect(reverse('pago'))  # Redirigir a la página de pago