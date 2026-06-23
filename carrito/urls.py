from django.urls import path
from . import views

urlpatterns = [
    path('agregar/<int:producto_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('eliminar_carrito/<str:item_id>/', views.eliminar_carrito, name='eliminar_carrito'),
    path('pago/', views.pago_views, name='pago'),
    path('pagoexitoso/', views.pago_exitoso_views, name='pago_exitoso'),
    
]