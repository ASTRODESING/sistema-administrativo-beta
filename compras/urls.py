from django.urls import path
from . import views

urlpatterns = [
    path("", views.panel, name="panelcompras"),
    path("ordencompra", views.orden_compras, name="ordencompras"),
    path("ordencompra/getorden/", views.historico_ordenes_compra, name="get_orden"),
    path("ordencompra/get_orden_document/<int:numero_orden>", views.get_pdf_orden, name="get_orden_document"),
    path("ordencompra/deleteorden/<int:numero_orden>", views.delete_ordenes_compra, name="delete_orden"),
    path("proveedores", views.proveedores, name="proveedores"),
    path("proveedores/editar/<int:id_proveedor>", views.editar_proveedores, name="proveedores_editar"),
    path("proveedores/eliminar/<int:id_proveedor>", views.eliminar_proveedores, name="proveedores_eliminar"),
    path("añadirproveedor", views.añadir_proveedor, name="añadir_proveedor"),

]
