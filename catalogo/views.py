from django.shortcuts import render
from .models import Categoria, Producto
# Create your views here.

def catalogo_view(request):
    productos = Producto.objects.all()
    
    contexto = {    
        'productos': productos
    }
    
    return render(request, 'catalogo/inicio.html', contexto)

def nosotros_view(request): 
    return render(request, 'catalogo/nosotros.html')

def menu_view(request):
    categorias = Categoria.objects.all()
    return render(request, 'catalogo/menu.html', {'categorias': categorias})

def ordernar_categorias_view(request, categoria_id):
    categoria = Categoria.objects.get(id=categoria_id)
    productos = Producto.objects.filter(categoria=categoria)
    
    contexto = {
        'categoria': categoria,
        'productos': productos
    }
    return render(request, 'catalogo/productos.html', contexto)

def cafe_views(request):
    return render(request, 'catalogo/nuestro-cafe.html')