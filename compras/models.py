from django.db import models

# Create your models here.
class Proveedor(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    direccion = models.TextField(default="Sin dirección")
    numero_telefono = models.IntegerField(default=000000000000)

class OrdenDeCompra(models.Model):
    numero_orden= models.AutoField(primary_key=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, to_field="id")
    descripcion = models.TextField(null=True)
    monto = models.BigIntegerField()