from django.contrib import admin
from .models import Categoria, Producto, Pedido, DetallePedido

admin.site.register(Categoria)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock')
    list_filter = ('categoria',)
    search_fields = ('nombre',)
    
admin.site.register(Producto, ProductoAdmin)

class detallePedido(admin.TabularInline):
    model = DetallePedido
    extra = 1
    
class pedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha_pedido', 'completado')
    list_filter = ('completado', 'fecha_pedido')
    inlines = [detallePedido]

admin.site.register(Pedido, pedidoAdmin)