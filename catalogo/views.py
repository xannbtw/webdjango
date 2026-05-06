from django.shortcuts import render
from .models import Producto
# Create your views here.

def catalogo_view(request):
    productos = Producto.objects.all()
    
    contexto = {
        'productos': productos
    }
    
    return render(request, 'catalogo/inicio.html', contexto)