from django.contrib import admin
from .models import Categoria, Producto, Pedido, ItemPedido

admin.site.register(Categoria)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock')
    list_filter = ('categoria',)
    search_fields = ('nombre',)


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ('producto', 'cantidad', 'tamano', 'tipo_leche')
    can_delete = False


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha_pedido', 'completado', 'num_items')
    list_filter = ('completado', 'fecha_pedido')
    readonly_fields = ('cliente', 'fecha_pedido')
    inlines = [ItemPedidoInline]

    def num_items(self, obj):
        return obj.itempedido_set.count()
    num_items.short_description = 'Items'
