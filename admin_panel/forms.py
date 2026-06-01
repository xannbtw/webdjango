from django import forms
from catalogo.models import Producto, Categoria


class ProductoForm(forms.ModelForm):
    """Formulario para crear y editar productos."""

    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'image', 'categoria']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        
        }

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio < 0:
            raise forms.ValidationError('El precio no puede ser negativo.')
        return precio

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is not None and stock < 0:
            raise forms.ValidationError('El stock no puede ser negativo.')
        return stock


class CategoriaForm(forms.ModelForm):
    """Formulario para crear y editar categorías."""

    class Meta:
        model = Categoria
        fields = ['nombre', 'image']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la categoría'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }


class BulkActionForm(forms.Form):
    """Formulario para acciones en lote sobre productos seleccionados."""
    ACTION_CHOICES = [
        ('', 'Seleccionar acción...'),
        ('delete', 'Eliminar seleccionados'),
        ('enable', 'Activar seleccionados'),
        ('disable', 'Desactivar seleccionados'),
    ]
    action = forms.ChoiceField(
        choices=ACTION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    selected_ids = forms.CharField(widget=forms.HiddenInput())
