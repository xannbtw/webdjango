from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    nombre = models.CharField( max_length=100)
    image = models.ImageField(upload_to='categorias/', null=True, blank=True)
    
    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.IntegerField()
    stock = models.IntegerField()
    image = models.ImageField(upload_to='productos/', null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    
    def __str__(self):
        return self.nombre
    
class Pedido(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    completado = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Pedido {self.id}'

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    cantidad = models.IntegerField(default=1)
    
    def __str__(self):
        return f'{self.cantidad} x {self.producto.nombre}'

class ItemPedido(models.Model):
    TAMANO_CHOICES = [
        ('Pequeño', 'Pequeño'),
        ('Mediano', 'Mediano'),
        ('Grande', 'Grande'),
    ]
    TIPO_LECHE_CHOICES = [
        ('Entera', 'Entera'),
        ('Descremada', 'Descremada'),
        ('Almendra', 'Almendra'),
        ('Avena', 'Avena'),
        ('Sin Leche', 'Sin Leche'),
    ]
    
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    tamano = models.CharField(max_length=20, choices=TAMANO_CHOICES, null=True, blank=True)
    tipo_leche = models.CharField(max_length=20, choices=TIPO_LECHE_CHOICES, null=True, blank=True)

    def __str__(self):
        opciones = []
        if self.tamano:
            opciones.append(self.tamano)
        if self.tipo_leche:
            opciones.append(self.tipo_leche)
            
        opciones_str = f" - Opciones: {', '.join(opciones)}" if opciones else ""
        return f"{self.cantidad} x {self.producto.nombre}{opciones_str}"