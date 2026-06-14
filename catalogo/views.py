from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from functools import wraps

from .models import Categoria, Producto
from .forms import ProductoForm, CategoriaForm
import mercadopago
from django.conf import settings


# ──────────────────────────────
#  Decorador admin
# ──────────────────────────────

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para acceder al panel de administración.')
            return redirect('admin_login')
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, 'No tienes permisos para acceder al panel de administración.')
            return redirect('/')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


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
#  Carrito
# ──────────────────────────────

def agregar_carrito(request, producto_id):
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id=producto_id)
        carrito = request.session.get('carrito', {})

        tamano = request.POST.get('tamano', '')
        tipo_leche = request.POST.get('tipo_leche', '')

        id_str = f"{producto_id}_{tamano}_{tipo_leche}" if (tamano or tipo_leche) else str(producto_id)

        if id_str in carrito:
            carrito[id_str]['cantidad'] += 1
        else:
            carrito[id_str] = {
                'producto_id': producto_id,
                'nombre': producto.nombre,
                'precio': producto.precio,
                'cantidad': 1,
                'tamano': tamano,
                'tipo_leche': tipo_leche,
                'imagen': producto.image.url if producto.image else '',
            }

        request.session['carrito'] = carrito
        messages.success(request, 'producto agregado.')
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
            'precio': item['precio'],
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


# ──────────────────────────────
#  Pago
# ──────────────────────────────

def pago_views(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        messages.warning(request, 'Tu carrito está vacío.')
        return redirect('ver_carrito')

    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

    items = []
    for key, item in carrito.items():
        items.append({
            "title": item['nombre'],
            "quantity": int(item['cantidad']),
            "unit_price": float(item['precio']),
            "currency_id": "CLP",
        })

    preference_data = {
        "items": items,
        "back_urls": {
            "success": "https://www.google.com",
            "failure": "https://www.google.com",
            "pending": "https://www.google.com",
        },
    }

    preference = sdk.preference().create(preference_data)

    if "response" not in preference or "init_point" not in preference["response"]:
        print("ERROR MP:", preference)
        messages.error(request, 'Error al conectar con Mercado Pago.')
        return redirect('ver_carrito')

    return redirect(preference["response"]["init_point"])

def pago_exitoso_views(request):
    request.session['carrito'] = {}
    messages.success(request, '¡Pago realizado con éxito! Gracias por tu compra.')
    return render(request, 'catalogo/pagoexitoso.html')


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


# ──────────────────────────────
#  Admin — Autenticación
# ──────────────────────────────

def admin_login(request):
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return redirect('admin_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff or user.is_superuser:
                login(request, user)
                messages.success(request, f'Bienvenido, {user.get_full_name() or user.username}.')
                return redirect(request.GET.get('next', 'admin_dashboard'))
            else:
                messages.error(request, 'No tienes permisos de administrador.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'admin_panel/login.html')

@admin_required
def admin_logout(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('admin_login')


# ──────────────────────────────
#  Admin — Dashboard
# ──────────────────────────────

@admin_required
def dashboard(request):
    total_productos = Producto.objects.count()
    total_categorias = Categoria.objects.count()

    por_categoria = (
        Categoria.objects.annotate(num_productos=Count('productos'))
        .order_by('-num_productos')[:5]
    )

    ultimos_productos = Producto.objects.select_related('categoria').order_by('-id')[:5]

    context = {
        'total_productos': total_productos,
        'productos_activos': total_productos,
        'productos_inactivos': 0,
        'total_categorias': total_categorias,
        'valor_inventario': 0,
        'por_categoria': por_categoria,
        'ultimos_productos': ultimos_productos,
        'sin_stock': Producto.objects.filter(stock=0).count(),
    }
    return render(request, 'admin_panel/dashboard.html', context)


# ──────────────────────────────
#  Admin — Productos
# ──────────────────────────────

@admin_required
def producto_lista(request):
    qs = Producto.objects.select_related('categoria').all()

    query = request.GET.get('q', '').strip()
    if query:
        qs = qs.filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(categoria__nombre__icontains=query)
        )

    cat_id = request.GET.get('categoria', '')
    if cat_id:
        qs = qs.filter(categoria_id=cat_id)

    order = request.GET.get('order', '-id')
    valid_orders = ['id', '-id', 'nombre', '-nombre', 'precio', '-precio']
    if order in valid_orders:
        qs = qs.order_by(order)

    paginator = Paginator(qs, 20)
    page = request.GET.get('page', 1)
    productos = paginator.get_page(page)

    categorias = Categoria.objects.all()

    context = {
        'productos': productos,
        'categorias': categorias,
        'query': query,
        'cat_id': cat_id,
        'order': order,
        'total_filtrado': qs.count(),
    }
    return render(request, 'admin_panel/producto_lista.html', context)

@admin_required
def producto_crear(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save()
            messages.success(request, f'Producto "{producto.nombre}" creado exitosamente.')
            if request.POST.get('guardar_y_nuevo'):
                return redirect('admin_producto_crear')
            return redirect('admin_producto_lista')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = ProductoForm()

    return render(request, 'admin_panel/producto_form.html', {
        'form': form,
        'titulo': 'Nuevo Producto',
        'accion': 'Crear',
    })

@admin_required
def producto_editar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, f'Producto "{producto.nombre}" actualizado correctamente.')
            return redirect('admin_producto_lista')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'admin_panel/producto_form.html', {
        'form': form,
        'producto': producto,
        'titulo': f'Editar: {producto.nombre}',
        'accion': 'Guardar cambios',
    })

@admin_required
def producto_eliminar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        nombre = producto.nombre
        producto.delete()
        messages.success(request, f'Producto "{nombre}" eliminado correctamente.')
        return redirect('admin_producto_lista')

    return render(request, 'admin_panel/confirmar_eliminar.html', {
        'objeto': producto,
        'tipo': 'producto',
        'nombre': producto.nombre,
        'cancelar_url': 'admin_producto_lista',
    })

@admin_required
@require_POST
def producto_bulk_action(request):
    action = request.POST.get('action')
    ids_raw = request.POST.get('selected_ids', '')

    try:
        ids = [int(i) for i in ids_raw.split(',') if i.strip().isdigit()]
    except ValueError:
        messages.error(request, 'Selección inválida.')
        return redirect('admin_producto_lista')

    if not ids:
        messages.warning(request, 'No seleccionaste ningún producto.')
        return redirect('admin_producto_lista')

    qs = Producto.objects.filter(pk__in=ids)

    if action == 'delete':
        count = qs.count()
        qs.delete()
        messages.success(request, f'{count} producto(s) eliminado(s) correctamente.')
    else:
        messages.warning(request, 'Acción no reconocida.')

    return redirect('admin_producto_lista')


# ──────────────────────────────
#  Admin — Categorías
# ──────────────────────────────

@admin_required
def categoria_lista(request):
    categorias = Categoria.objects.annotate(
        num_productos=Count('productos')
    ).order_by('nombre')

    query = request.GET.get('q', '').strip()
    if query:
        categorias = categorias.filter(nombre__icontains=query)

    paginator = Paginator(categorias, 20)
    page = request.GET.get('page', 1)
    categorias_page = paginator.get_page(page)

    return render(request, 'admin_panel/categoria_lista.html', {
        'categorias': categorias_page,
        'query': query,
    })

@admin_required
def categoria_crear(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'Categoría "{categoria.nombre}" creada exitosamente.')
            return redirect('admin_categoria_lista')
        else:
            messages.error(request, 'Por favor corrige los errores.')
    else:
        form = CategoriaForm()

    return render(request, 'admin_panel/categoria_form.html', {
        'form': form,
        'titulo': 'Nueva Categoría',
        'accion': 'Crear',
    })

@admin_required
def categoria_editar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)

    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, f'Categoría "{categoria.nombre}" actualizada.')
            return redirect('admin_categoria_lista')
        else:
            messages.error(request, 'Por favor corrige los errores.')
    else:
        form = CategoriaForm(instance=categoria)

    return render(request, 'admin_panel/categoria_form.html', {
        'form': form,
        'categoria': categoria,
        'titulo': f'Editar: {categoria.nombre}',
        'accion': 'Guardar cambios',
    })

@admin_required
def categoria_eliminar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)

    if request.method == 'POST':
        nombre = categoria.nombre
        if categoria.productos.exists():
            messages.error(
                request,
                f'No puedes eliminar "{nombre}" porque tiene productos asociados. '
                'Reasigna o elimina esos productos primero.'
            )
            return redirect('admin_categoria_lista')
        categoria.delete()
        messages.success(request, f'Categoría "{nombre}" eliminada correctamente.')
        return redirect('admin_categoria_lista')

    return render(request, 'admin_panel/confirmar_eliminar.html', {
        'objeto': categoria,
        'tipo': 'categoría',
        'nombre': categoria.nombre,
        'cancelar_url': 'admin_categoria_lista',
        'advertencia': (
            f'Esta categoría tiene {categoria.productos.count()} producto(s) asociado(s).'
            if categoria.productos.exists() else None
        ),
    })
