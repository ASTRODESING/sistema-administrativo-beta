from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.http import FileResponse

class Categoria(models.Model):
    nombre= models.CharField(max_length=200, unique=True)
    destacado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre
    class Meta:
        db_table='categorias'
        verbose_name= 'Categoria'
        verbose_name_plural='Categorías'
        ordering= ['-id']


class Producto(models.Model):
    slug = AutoSlugField(populate_from='nombre', unique=True)
    codigo_de_barras = models.CharField(max_length=13, unique=True, default='0000000000000')
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField(max_length=1000, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    precio_venta = models.DecimalField(max_digits=6, decimal_places=2)
    precio_compra = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField()
    cantidad_comprada = models.PositiveIntegerField(default=0)
    cantidad_vendida = models.PositiveIntegerField(default=0)
    exento_de_impuesto = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nombre

    class Meta:
        db_table='producto'
        verbose_name= 'Producto'
        verbose_name_plural='Productos'
        ordering= ['id']


