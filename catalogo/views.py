from django.shortcuts import render
from .models import Producto
# Create your views here.

def catalogo_view(request):
    productos = Producto.objects.all()
    
    contexto = {
        'productos': productos
    }
    
    return render(request, 'catalogo/inicio.html', contexto)

def nosotros_view(request): 
    return render(request, 'catalogo/nosotros.html')