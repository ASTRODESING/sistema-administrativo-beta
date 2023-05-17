from django.contrib import admin
from .models import Cliente, Factura, FormasDePago

admin.site.register(Cliente)
admin.site.register(Factura)
admin.site.register(FormasDePago)
