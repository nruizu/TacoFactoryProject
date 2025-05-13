#Autor: Samuel Gutierrez

import json
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from .models import Carrito, CarritoPlato, CarritoBebida, Plato, Bebida
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def calcular_y_guardar_subtotal(request, carrito):
    platos = CarritoPlato.objects.filter(carrito=carrito)
    bebidas = CarritoBebida.objects.filter(carrito=carrito)
    subtotal = sum(item.plato.precio * item.cantidad for item in platos) + \
               sum(item.bebida.precio * item.cantidad for item in bebidas)
    request.session['monto'] = subtotal
    return subtotal

@login_required
def ver_carrito(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    platos = CarritoPlato.objects.filter(carrito=carrito)
    bebidas = CarritoBebida.objects.filter(carrito=carrito)

    # Calcular el subtotal
    subtotal = calcular_y_guardar_subtotal(request, carrito)

    context = {
        'carrito': carrito,
        'platos': platos,
        'bebidas': bebidas,
        'subtotal': subtotal,
    }

    return render(request, 'carrito.html', context)

@csrf_exempt
def agregar_al_carrito(request):
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "redirect": "/login/?next=" + request.path}, status=401)

    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

    try:
        data = json.loads(request.body.decode('utf-8'))
        tipo = data.get("tipo")
        item_id = data.get("item_id")
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "message": "Error en formato JSON"}, status=400)

    if not tipo or not item_id:
        return JsonResponse({"success": False, "message": "Datos incompletos"}, status=400)

    if tipo == "plato":
        plato = get_object_or_404(Plato, pk=item_id)
        carrito_item, created = CarritoPlato.objects.get_or_create(carrito=carrito, plato=plato)
    elif tipo == "bebida":
        bebida = get_object_or_404(Bebida, pk=item_id)
        carrito_item, created = CarritoBebida.objects.get_or_create(carrito=carrito, bebida=bebida)

    else:
        return JsonResponse({"success": False, "message": "Tipo de producto inválido"}, status=400)

    if not created:
        carrito_item.cantidad += 1
        carrito_item.save()

    subtotal = calcular_y_guardar_subtotal(request, carrito)

    return JsonResponse({
        "success": True,
        "message": "Producto agregado al carrito",
        "cantidad": carrito_item.cantidad,
        "subtotal": subtotal
    })

@login_required
def eliminar_del_carrito(request, tipo, item_id):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    
    if tipo == "plato":
        item = get_object_or_404(CarritoPlato, carrito=carrito, id=item_id)
        
    elif tipo == "bebida":
        item = get_object_or_404(CarritoBebida, carrito=carrito, id=item_id)
        
    item.delete()
    calcular_y_guardar_subtotal(request, carrito)
    
    return JsonResponse({"success": True, "message": "Producto eliminado del carrito"})

@csrf_exempt
@login_required
def actualizar_cantidad(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            tipo = data.get("tipo")
            item_id = data.get("item_id")
            cantidad = int(data.get("cantidad", 1))
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato JSON inválido'}, status=400)

        carrito = get_object_or_404(Carrito, usuario=request.user)
        
        try:
            if tipo == "plato":
                item = get_object_or_404(CarritoPlato, carrito=carrito, id=item_id)
            elif tipo == "bebida":
                item = get_object_or_404(CarritoBebida, carrito=carrito, id=item_id)
            else:
                return JsonResponse({'error': 'Tipo inválido'}, status=400)
        except (CarritoPlato.DoesNotExist, CarritoBebida.DoesNotExist):
            return JsonResponse({'error': 'El producto ya no está en el carrito'}, status=404)

        if cantidad <= 0:
            item.delete()
            eliminado = True
            nueva_cantidad = 0
        else:
            item.cantidad = cantidad
            item.save()
            eliminado = False
            nueva_cantidad = item.cantidad
            
        subtotal = calcular_y_guardar_subtotal(request, carrito)
        
        return JsonResponse({
            "success": True,
            "nueva_cantidad": nueva_cantidad,
            "eliminado": eliminado,
            "subtotal": subtotal
        })

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
def vaciar_carrito(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    CarritoPlato.objects.filter(carrito=carrito).delete()
    CarritoBebida.objects.filter(carrito=carrito).delete()
    
    calcular_y_guardar_subtotal(request, carrito)
    return redirect('ver_carrito')

@login_required
def proceder_pago(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    monto = calcular_y_guardar_subtotal(request, carrito)
    
    if monto <= 0:
        return redirect('ver_carrito')

    return redirect(reverse('pago'))