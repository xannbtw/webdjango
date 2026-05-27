from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalogo_view, name='inicio'), 
    path('nosotros/', views.nosotros_view, name='nosotros'),
    path('menu/', views.menu_view, name='menu'),
    path('categoria/<int:categoria_id>/', views.ordernar_categorias_view, name='filtro_categoria'),
    path('nuestro-cafe/', views.cafe_views, name='nuestro_cafe'),
    path('ubicacion/', views.ubi_views, name='ubicacion'),
    path('agregar/<int:producto_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('eliminar_carrito/<str:item_id>/', views.eliminar_carrito, name='eliminar_carrito'),
    path('pago.html/', views.pago_views, name='pago'),
    path('pagoexitoso/', views.pago_exitoso_views, name='pago_exitoso'),
]