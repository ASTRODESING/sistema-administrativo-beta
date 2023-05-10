from django.urls import path
from . import views

urlpatterns = [
    path("", views.panel, name="panelcompras"),
    path("ordencompra", views.orden_compras, name="ordencompras"),
    path("añadirproveedor", views.añadir_proveedor, name="añadir_proveedor"),

]
