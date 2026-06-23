from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from catalogo.models import Producto, Pedido, ItemPedido

# Create your views here.

AJUSTE_TAMANO = {
    'Pequeño': -200,
    'Mediano': 0,
    'Grande': 500,
    '': 0,
}

def precio_con_tamano(precio_base, tamano):
    return precio_base + AJUSTE_TAMANO.get(tamano, 0)

def agregar_carrito(request, producto_id):
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id=producto_id)
        carrito = request.session.get('carrito', {})

        tamano = request.POST.get('tamano', '')
        tipo_leche = request.POST.get('tipo_leche', '')

        # Precio final ya con ajuste de tamaño aplicado
        precio_final = precio_con_tamano(producto.precio, tamano)

        id_str = f"{producto_id}_{tamano}_{tipo_leche}" if (tamano or tipo_leche) else str(producto_id)

        if id_str in carrito:
            carrito[id_str]['cantidad'] += 1
        else:
            carrito[id_str] = {
                'producto_id': producto_id,
                'nombre': producto.nombre,
                'precio_base': producto.precio,
                'precio': precio_final,
                'cantidad': 1,
                'tamano': tamano,
                'tipo_leche': tipo_leche,
                'imagen': producto.image.url if producto.image else '',
            }

        request.session['carrito'] = carrito
        messages.success(request, 'Producto agregado correctamente.')
        next_url = request.POST.get('next', 'menu')
        return redirect(next_url)
    return redirect('inicio')


def ver_carrito(request):
    carrito = request.session.get('carrito', {})

    total_carrito = 0
    carrito_list = []

    for key, item in carrito.items():
        precio = item['precio']
        cantidad = item['cantidad']
        subtotal = precio * cantidad
        total_carrito += subtotal

        carrito_list.append({
            'id': key,
            'nombre': item['nombre'],
            'precio_base': item.get('precio_base', item['precio']),
            'precio': precio,
            'cantidad': cantidad,
            'subtotal': subtotal,
            'tamano': item.get('tamano', ''),
            'tipo_leche': item.get('tipo_leche', ''),
            'imagen': item.get('imagen', ''),
        })

    context = {'carrito_list': carrito_list, 'total_carrito': total_carrito}
    return render(request, 'catalogo/carrito.html', context)


def eliminar_carrito(request, item_id):
    carrito = request.session.get('carrito', {})
    id_str = str(item_id)
    if id_str in carrito:
        del carrito[id_str]
        request.session['carrito'] = carrito
        messages.info(request, 'producto eliminado')
    return redirect('ver_carrito')

def pago_views(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Debes iniciar sesión para proceder con la compra.')
        return redirect('inicio')

    carrito = request.session.get('carrito', {})
    if not carrito:
        messages.warning(request, 'Tu carrito está vacío.')
        return redirect('ver_carrito')

    total_carrito = sum(item['precio'] * item['cantidad'] for item in carrito.values())

    if request.method == 'POST':
        nombre_titular = request.POST.get('nombre_titular', '').strip()
        numero_tarjeta = request.POST.get('numero_tarjeta', '').strip()
        fecha_exp = request.POST.get('fecha_exp', '').strip()
        cvv = request.POST.get('cvv', '').strip()

        if not all([nombre_titular, numero_tarjeta, fecha_exp, cvv]):
            messages.error(request, 'Por favor completa todos los campos.')
            return render(request, 'catalogo/pago.html', {
                'carrito_list': _build_carrito_list(carrito),
                'total_carrito': total_carrito,
            })

        pedido = Pedido.objects.create(
            cliente=request.user,
            completado=True,
        )

        for key, item in carrito.items():
            try:
                producto = Producto.objects.get(id=item['producto_id'])
                ItemPedido.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=item['cantidad'],
                    tamano=item.get('tamano') or None,
                    tipo_leche=item.get('tipo_leche') or None,
                    precio_unitario=item['precio'],
                )
            except Producto.DoesNotExist:
                pass

        request.session['carrito'] = {}
        request.session['ultimo_pedido_id'] = pedido.id

        return redirect('pago_exitoso')

    carrito_list = _build_carrito_list(carrito)
    return render(request, 'catalogo/pago.html', {
        'carrito_list': carrito_list,
        'total_carrito': total_carrito,
    })


def _build_carrito_list(carrito):
    result = []
    for key, item in carrito.items():
        subtotal = item['precio'] * item['cantidad']
        result.append({
            'id': key,
            'nombre': item['nombre'],
            'precio_base': item.get('precio_base', item['precio']),
            'precio': item['precio'],
            'cantidad': item['cantidad'],
            'subtotal': subtotal,
            'tamano': item.get('tamano', ''),
            'tipo_leche': item.get('tipo_leche', ''),
            'imagen': item.get('imagen', ''),
        })
    return result


def pago_exitoso_views(request):
    pedido_id = request.session.pop('ultimo_pedido_id', None)
    return render(request, 'catalogo/pagoexitoso.html', {'pedido_id': pedido_id})