from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from functools import wraps

from .models import Categoria, Producto, Pedido, ItemPedido
from .forms import ProductoForm, CategoriaForm


# ──────────────────────────────
#  Ajuste de precio por tamaño
# ──────────────────────────────

# ──────────────────────────────
#  Vistas públicas del catálogo
# ──────────────────────────────
def catalogo_view(request):
    productos = Producto.objects.all()
    contexto = {'productos': productos}
    return render(request, 'catalogo/inicio.html', contexto)

def nosotros_view(request):
    return render(request, 'catalogo/nosotros.html')

def menu_view(request):
    categorias = Categoria.objects.all()
    return render(request, 'catalogo/menu.html', {'categorias': categorias})

def ordernar_categorias_view(request, categoria_id):
    categoria = Categoria.objects.get(id=categoria_id)
    productos = Producto.objects.filter(categoria=categoria)
    contexto = {'categoria': categoria, 'productos': productos}
    return render(request, 'catalogo/productos.html', contexto)

def cafe_views(request):
    return render(request, 'catalogo/nuestro-cafe.html')

def ubi_views(request):
    return render(request, 'catalogo/ubicacion.html')

# ──────────────────────────────
#  Autenticación pública
# ──────────────────────────────
def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})