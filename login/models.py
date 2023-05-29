from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Usuario(User):
    is_gerente= models.BooleanField(default=False)
    is_cajero= models.BooleanField(default=True)

class PrecioDolar(models.Model):
    precio= models.FloatField(default=1)

class DatosEmpresa(models.Model):
    nombre = models.CharField(max_length=255)
    direccion = models.TextField()
    telefono = models.IntegerField()
    correo = models.EmailField()
    ci_rif = models.IntegerField(default=0)