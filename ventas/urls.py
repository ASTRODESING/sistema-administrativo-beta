from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.panel, name="panel_ventas"),
    path('caja', views.caja, name="caja"),
    path('factura', views.facturas, name="facturas"),
    path('factura/getfactura/<int:numero_factur>', views.get_factura, name="getfactura"),
    path('clientes', views.clientes, name="clientes"),
    path('clientes/nuevocliente', views.nuevo_cliente, name="nuevocliente"),
    path('clientes/editcliente/<int:id_cliente>', views.edit_cliente, name="editcliente"),
    path('clientes/eliminarcliente/<int:id_cliente>', views.elimnar_cliente, name="eliminarcliente"),
    path('getproducto/<int:id_producto>', views.get_productos, name="get_Productos"),
    path('imprimirfactura', views.imprimir_pdf , name="imprimir_pdf")
]