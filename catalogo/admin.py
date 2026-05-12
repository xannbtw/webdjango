from django.contrib import admin
from .models import Categoria, Producto, Pedido, DetallePedido

admin.site.register(Categoria) # añade categoria al panel de admin

class ProductoAdmin(admin.ModelAdmin): 
    list_display = ('nombre', 'categoria', 'precio', 'stock') # variables para crear el producto en el panel
    list_filter = ('categoria',) # agrega categoria al panel lateral
    search_fields = ('nombre',) # agrega una busqueda por nombre
    
admin.site.register(Producto, ProductoAdmin) # agregar Producto con la clase ProductoAdmin al panel

class detallePedido(admin.TabularInline): # para editar prod en la parte de pedido
    model = DetallePedido
    extra = 1 # espacio en blanco para nuevo producto al pedido
    
class pedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha_pedido', 'completado') # columnas que se ven en pedidos
    list_filter = ('completado', 'fecha_pedido') # filtros laterales de fecha y estado
    inlines = [detallePedido] # se inserta detallePedido en la pantalla del pedido

admin.site.register(Pedido, pedidoAdmin) # agregar Pedido y pedidoAdmin al panel