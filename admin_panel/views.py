from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from catalogo.models import Producto, Categoria
from .forms import ProductoForm, CategoriaForm
from .decorators import admin_required


# ──────────────────────────────
#  Autenticación
# ──────────────────────────────

def admin_login(request):
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return redirect('admin_panel:dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff or user.is_superuser:
                login(request, user)
                messages.success(request, f'Bienvenido, {user.get_full_name() or user.username}.')
                return redirect(request.GET.get('next', 'admin_panel:dashboard'))
            else:
                messages.error(request, 'No tienes permisos de administrador.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'admin_panel/login.html')


@admin_required
def admin_logout(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('admin_panel:login')


# ──────────────────────────────
#  Dashboard
# ──────────────────────────────

@admin_required
def dashboard(request):
    total_productos = Producto.objects.count()
    total_categorias = Categoria.objects.count()

    # Productos por categoría
    por_categoria = (
        Categoria.objects.annotate(num_productos=Count('productos'))
        .order_by('-num_productos')[:5]
    )

    # Últimos productos añadidos
    ultimos_productos = Producto.objects.select_related('categoria').order_by('-id')[:5]

    context = {
        'total_productos': total_productos,
        'productos_activos': total_productos,  # no hay campo disponible
        'productos_inactivos': 0,
        'total_categorias': total_categorias,
        'valor_inventario': 0,
        'por_categoria': por_categoria,
        'ultimos_productos': ultimos_productos,
        'sin_stock': Producto.objects.filter(stock=0).count(),
    }
    return render(request, 'admin_panel/dashboard.html', context)

# ──────────────────────────────
#  Productos
# ──────────────────────────────

@admin_required
def producto_lista(request):
    qs = Producto.objects.select_related('categoria').all()

    # Búsqueda
    query = request.GET.get('q', '').strip()
    if query:
        qs = qs.filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(categoria__nombre__icontains=query)
        )

    # Filtro por categoría
    cat_id = request.GET.get('categoria', '')
    if cat_id:
        qs = qs.filter(categoria_id=cat_id)

    # Ordenamiento
    order = request.GET.get('order', '-id')
    valid_orders = ['id', '-id', 'nombre', '-nombre', 'precio', '-precio']
    if order in valid_orders:
        qs = qs.order_by(order)

    # Paginación
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
                return redirect('admin_panel:producto_crear')
            return redirect('admin_panel:producto_lista')
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
            return redirect('admin_panel:producto_lista')
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
        return redirect('admin_panel:producto_lista')

    return render(request, 'admin_panel/confirmar_eliminar.html', {
        'objeto': producto,
        'tipo': 'producto',
        'nombre': producto.nombre,
        'cancelar_url': 'admin_panel:producto_lista',
    })




@admin_required
@require_POST
def producto_bulk_action(request):
    """Acciones en lote: eliminar, activar, desactivar."""
    action = request.POST.get('action')
    ids_raw = request.POST.get('selected_ids', '')

    try:
        ids = [int(i) for i in ids_raw.split(',') if i.strip().isdigit()]
    except ValueError:
        messages.error(request, 'Selección inválida.')
        return redirect('admin_panel:producto_lista')

    if not ids:
        messages.warning(request, 'No seleccionaste ningún producto.')
        return redirect('admin_panel:producto_lista')

    qs = Producto.objects.filter(pk__in=ids)

    if action == 'delete':
        count = qs.count()
        qs.delete()
        messages.success(request, f'{count} producto(s) eliminado(s) correctamente.')
    elif action == 'enable':
        count = qs.update(disponible=True)
        messages.success(request, f'{count} producto(s) activado(s) correctamente.')
    elif action == 'disable':
        count = qs.update(disponible=False)
        messages.success(request, f'{count} producto(s) desactivado(s) correctamente.')
    else:
        messages.warning(request, 'Acción no reconocida.')

    return redirect('admin_panel:producto_lista')


# ──────────────────────────────
#  Categorías
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
            return redirect('admin_panel:categoria_lista')
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
            return redirect('admin_panel:categoria_lista')
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
            return redirect('admin_panel:categoria_lista')
        categoria.delete()
        messages.success(request, f'Categoría "{nombre}" eliminada correctamente.')
        return redirect('admin_panel:categoria_lista')

    return render(request, 'admin_panel/confirmar_eliminar.html', {
        'objeto': categoria,
        'tipo': 'categoría',
        'nombre': categoria.nombre,
        'cancelar_url': 'admin_panel:categoria_lista',
        'advertencia': (
            f'Esta categoría tiene {categoria.productos.count()} producto(s) asociado(s).'
            if categoria.productos.exists() else None
        ),
    })