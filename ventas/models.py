from django.db import models
from django.utils import timezone

# Create your models here.
class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre= models.CharField(max_length=255)
    ci_rif = models.IntegerField(default=0)
    
class FormasDePago(models.Model):
    forma = models.CharField(max_length=255, unique=True)

class Factura(models.Model):
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE,to_field="id")
    numero_factura = models.AutoField(default=0, primary_key=True)
    fecha_creacion = models.DateField( default=timezone.now)
    monto = models.IntegerField(default=0)
    usuario = models.CharField(default="No User Data",max_length=150)
    documento = models.FileField(null=True)
    forma_de_pago = models.ForeignKey(FormasDePago, on_delete=models.CASCADE, to_field="forma", default=1)
    
