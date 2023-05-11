from django.shortcuts import render, HttpResponse
from .models import OrdenDeCompra, Proveedor

# Create your views here.
def panel(request):
    return render(request,"panel-compras.html")

def orden_compras(request):
    if request.method== "GET":
        proveedores = Proveedor.objects.all()
        return render(request,"ordencompra.html", {"proveedores": proveedores})
    else:
        print(request.POST)
        proveedores = Proveedor.objects.all()
        return render(request,"ordencompra.html", {"proveedores": proveedores})
    
def añadir_proveedor(request):
    if request.method== "GET":
        return render(request,"añadir_proveedor.html")
    else:
        try:
            nuevo_proveedor = Proveedor.objects.create(
                nombre = request.POST["nombre"],
                direccion = request.POST["direccion"],
                numero_telefono = request.POST["telefono"]
            )
            nuevo_proveedor.save()
            status = "Proveedor Creado Satisfactoriamente"
            return render(request,"añadir_proveedor.html", {"status":status})
        except:
            status = "Ha ocurrido un error"
            return render(request,"añadir_proveedor.html", {"status":status})