from django.urls import path
from . import views

urlpatterns = [
    # ── Catálogo público ──────────────────────────────────
    path('', views.catalogo_view, name='inicio'),
    path('nosotros/', views.nosotros_view, name='nosotros'),
    path('menu/', views.menu_view, name='menu'),
    path('categoria/<int:categoria_id>/', views.ordernar_categorias_view, name='filtro_categoria'),
    path('nuestro-cafe/', views.cafe_views, name='nuestro_cafe'),
    path('ubicacion/', views.ubi_views, name='ubicacion'),

    # ── Carrito ───────────────────────────────────────────
    path('agregar/<int:producto_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('eliminar_carrito/<str:item_id>/', views.eliminar_carrito, name='eliminar_carrito'),
    path('pago/', views.pago_views, name='pago'),
    path('pagoexitoso/', views.pago_exitoso_views, name='pago_exitoso'),

    # ── Admin — Autenticación ─────────────────────────────
    path('admin-panel/login/', views.admin_login, name='admin_login'),
    path('admin-panel/logout/', views.admin_logout, name='admin_logout'),

    # ── Admin — Dashboard ─────────────────────────────────
    path('admin-panel/', views.dashboard, name='admin_dashboard'),

    # ── Admin — Pedidos ───────────────────────────────────
    path('admin-panel/pedidos/', views.pedido_lista, name='admin_pedido_lista'),
    path('admin-panel/pedidos/<int:pk>/', views.pedido_detalle, name='admin_pedido_detalle'),

    # ── Admin — Productos ─────────────────────────────────
    path('admin-panel/productos/', views.producto_lista, name='admin_producto_lista'),
    path('admin-panel/productos/nuevo/', views.producto_crear, name='admin_producto_crear'),
    path('admin-panel/productos/<int:pk>/editar/', views.producto_editar, name='admin_producto_editar'),
    path('admin-panel/productos/<int:pk>/eliminar/', views.producto_eliminar, name='admin_producto_eliminar'),
    path('admin-panel/productos/bulk/', views.producto_bulk_action, name='admin_producto_bulk'),

    # ── Admin — Categorías ────────────────────────────────
    path('admin-panel/categorias/', views.categoria_lista, name='admin_categoria_lista'),
    path('admin-panel/categorias/nueva/', views.categoria_crear, name='admin_categoria_crear'),
    path('admin-panel/categorias/<int:pk>/editar/', views.categoria_editar, name='admin_categoria_editar'),
    path('admin-panel/categorias/<int:pk>/eliminar/', views.categoria_eliminar, name='admin_categoria_eliminar'),
]
