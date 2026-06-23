from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('', views.dashboard, name='admin_dashboard'), # Al entrar a /admin-panel/ cargará esto
    path('pedidos/', views.pedido_lista, name='admin_pedido_lista'),
    path('pedidos/<int:pk>/', views.pedido_detalle, name='admin_pedido_detalle'),
    path('productos/', views.producto_lista, name='admin_producto_lista'),
    path('productos/nuevo/', views.producto_crear, name='admin_producto_crear'),
    path('productos/<int:pk>/editar/', views.producto_editar, name='admin_producto_editar'),
    path('productos/<int:pk>/eliminar/', views.producto_eliminar, name='admin_producto_eliminar'),
    path('productos/bulk/', views.producto_bulk_action, name='admin_producto_bulk'),
    path('categorias/', views.categoria_lista, name='admin_categoria_lista'),
    path('categorias/nueva/', views.categoria_crear, name='admin_categoria_crear'),
    path('categorias/<int:pk>/editar/', views.categoria_editar, name='admin_categoria_editar'),
    path('categorias/<int:pk>/eliminar/', views.categoria_eliminar, name='admin_categoria_eliminar'),
]