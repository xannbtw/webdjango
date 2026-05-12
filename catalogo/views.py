from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Categoria, Producto
# Create your views here.

def catalogo_view(request):
    productos = Producto.objects.all()# se traen todos los productos de la bd.
    
    contexto = {    
        'productos': productos # se prepara el diccionario para mandarlo al html.
    }
    
    return render(request, 'catalogo/inicio.html', contexto) # se muestra la pagina de inicio.

def nosotros_view(request): 
    return render(request, 'catalogo/nosotros.html')# vista de nosotros.

def menu_view(request):
    categorias = Categoria.objects.all() # se traen todas las categorias de la bd.
    return render(request, 'catalogo/menu.html', {'categorias': categorias}) # se mandan las categorias al menu.

def ordernar_categorias_view(request, categoria_id):
    categoria = Categoria.objects.get(id=categoria_id) # se busca la categoria.
    productos = Producto.objects.filter(categoria=categoria) # buscan los productos que pertenecen a esa categoria.
    
    contexto = {
        'categoria': categoria,
        'productos': productos
    }
    return render(request, 'catalogo/productos.html', contexto) # se muestran los productos filtrados.

def cafe_views(request):
    return render(request, 'catalogo/nuestro-cafe.html') # vista de nuestro cafe

def ubi_views(request):
    return render(request, 'catalogo/ubicacion.html') # vista de la ubi

def agregar_carrito(request, producto_id):
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id=producto_id) # se busca el producto.
        carrito = request.session.get('carrito', {}) # si el cliente tiene un carrito se usa, si no se crea uno vacio.
        id_str = str(producto_id) # se guarda el id como string.
        if id_str in carrito:
            carrito[id_str]['cantidad'] += 1 #si ya esta el prod en el carro se suma 1.
        else: # si no esta, se agrega con los datos.
            carrito[id_str] = {
                'producto_id': producto_id,
                'nombre': producto.nombre,
                'precio': producto.precio,
                'cantidad': 1,
            }
            
        request.session['carrito'] = carrito # se guarda el carrito actualizado
        messages.success(request, 'producto agregado.')
        return redirect('menu') # se redirige al menu
    return redirect('inicio')

def ver_carrito(request):
    carrito = request.session.get('carrito', {}) # Traemos el carrito de la sesion
    total_carrito = 0
    carrito_list = []
    
    for key, item in carrito.items(): # Recorremos lo que hay guardado para sacar las cuentas
        precio = item['precio']
        cantidad = item['cantidad']
        subtotal = precio * cantidad # se multiplica para el subtotal
        
        total_carrito += subtotal
        
        # Armamos una lista ordenada para el html
        carrito_list.append({
            'id': key,
            'nombre': item['nombre'],
            'precio': item['precio'],
            'cantidad': cantidad,
            'subtotal': subtotal
        })
        
    context = {
        'carrito_list': carrito_list,
        'total_carrito': total_carrito,
    }
    return render(request, 'catalogo/carrito.html', context)