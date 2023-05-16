from django.urls import path
from . import views

urlpatterns = [
    path("", views.panel, name="panelcompras"),
    path("ordencompra", views.orden_compras, name="ordencompras"),
    path("ordencompra/getorden/", views.historico_ordenes_compra, name="get_orden"),
    path("ordencompra/get_orden_document/<int:numero_orden>", views.get_pdf_orden, name="get_orden_document"),
    path("ordencompra/deleteorden/<int:numero_orden>", views.delete_ordenes_compra, name="delete_orden"),
    path("añadirproveedor", views.añadir_proveedor, name="añadir_proveedor"),

]
