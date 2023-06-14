from django.db import models
from django.utils import timezone
from datetime import date

# Create your models here.
class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre= models.CharField(max_length=255)
    ci_rif = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.nombre
    
class FormasDePago(models.Model):
    forma = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.forma

class Factura(models.Model):
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE,to_field="id")
    numero_factura = models.AutoField(primary_key=True)
    fecha_creacion = models.DateField( default=timezone.now)
    monto = models.IntegerField(default=0)
    usuario = models.CharField(default="No User Data",max_length=150)
    documento = models.FileField(null=True, upload_to='documents/facturas')
    forma_de_pago = models.ForeignKey(FormasDePago, on_delete=models.CASCADE, to_field="forma", default=1)
    referencia = models.IntegerField(null=True)

    def __str__(self) -> str:
        return str(self.numero_factura)

class Ganancias(models.Model):
    
    año = models.IntegerField(default= date.today().year)
    mes = models.IntegerField(default= date.today().month)
    dia = models.IntegerField(default= date.today().day)
    ganancia = models.PositiveBigIntegerField(null=True)

class NumeroDeClientes(models.Model):
    año = models.IntegerField(default= date.today().year)
    mes = models.IntegerField(default= date.today().month)
    dia = models.IntegerField(default= date.today().day)
    numero_clientes = models.BigIntegerField(null=True)