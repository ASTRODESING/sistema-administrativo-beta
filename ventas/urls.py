from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Panel, name="panel_ventas"),
    path('caja', views.Caja, name="caja"),
    path('factura', views.Facturas, name="facturas"),
    path('factura/getfactura/<int:numero_factur>', views.get_Factura, name="getfactura"),
    path('clientes', views.Clientes, name="clientes"),
    path('clientes/nuevocliente', views.NuevoCliente, name="nuevocliente"),
    path('clientes/editcliente/<int:id_cliente>', views.EditCliente, name="editcliente"),
    path('clientes/eliminarcliente/<int:id_cliente>', views.ElimnarCliente, name="eliminarcliente"),
    path('getproducto/<int:id_producto>', views.get_Productos, name="get_Productos"),
    path('imprimirfactura', views.imprimir_pdf , name="imprimir_pdf")
]