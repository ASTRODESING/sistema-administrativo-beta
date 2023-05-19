from django.db import models
from django.utils import timezone
from datetime import date

# Create your models here.
class Proveedor(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    direccion = models.TextField(default="Sin dirección")
    numero_telefono = models.IntegerField(default=000000000000)

    def __str__(self) -> str:
        return self.nombre

class OrdenDeCompra(models.Model):
    numero_orden= models.AutoField(primary_key=True)
    fecha_orden = models.DateField( default=timezone.now)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, to_field="id")
    archivo = models.FileField(null=True, upload_to='documents/ordenescompra')
    monto = models.BigIntegerField()

    def __str__(self) -> str:
        return self.numero_orden
    
class Perdida(models.Model):
    
    año = models.IntegerField(default= date.today().year, primary_key=True)
    mes = models.IntegerField(default= date.today().month, primary_key=True)
    dia = models.IntegerField(default= date.today().day, primary_key=True)
    perdida = models.BigIntegerField(null=True)
