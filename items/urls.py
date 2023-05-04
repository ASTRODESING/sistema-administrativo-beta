from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Inventario, name="inventario"),
    path('<int:producto_id>', views.EditarProducto, name="editarproducto"),
    path('categorias', views.Categorias, name="productoid"),
    path('<int:producto_id>/delete', views.ElimnarProd, name="eliminarprod"),
]