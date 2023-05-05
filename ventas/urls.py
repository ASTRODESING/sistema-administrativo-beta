from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Panel, name="panel_ventas"),
    path('caja', views.Caja, name="caja"),
    path('reportes', views.Reportes, name="reportes"),
    path('clientes', views.Clientes, name="clientes"),
    path('clientes/nuevocliente', views.EditCliente, name="editcliente"),
    path('clientes/editcliente/<int:id_cliente>', views.EditCliente, name="editcliente"),
    path('getproducto/<int:id_producto>', views.get_Productos, name="get_Productos"),
    path('imprimirfactura', views.imprimir_pdf , name="imprimir_pdf")
]