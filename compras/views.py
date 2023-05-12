from django.shortcuts import render, HttpResponse
from django.template.loader import get_template
from .models import OrdenDeCompra, Proveedor
from io import BytesIO
from weasyprint import HTML
from datetime import datetime

# Create your views here.
def panel(request):
    return render(request, "panel-compras.html")


def orden_compras(request):
    if request.method == "GET":
        proveedores = Proveedor.objects.all()
        return render(request, "ordencompra.html", {"proveedores": proveedores})
    else:
        datos = []
        nombres = request.POST.getlist("nombre_producto")
        print(request.POST)
        precios = request.POST.getlist("precio")
        cantidades = request.POST.getlist("cantidad")
        subtotal_productos = 0

        contador = 0

        for precio in precios:
            subtotal_producto = int(precio) * int(cantidades[contador])
            subtotal_productos += subtotal_producto
            datos.append(
                {
                    "producto": nombres[contador],
                    "precio": precio,
                    "cantidad": cantidades[contador],
                    "subtotal_producto": subtotal_producto,
                }
            )

            contador += 1

        total = int(request.POST["presupuesto"]) - subtotal_productos
        template = get_template("pdf_ordendecompra.html")


        nueva_orden_compra = OrdenDeCompra.objects.create(
            proveedor = request.POST["proveedor_id"],
            monto = total
        )
        nueva_orden_compra.save()


        html = template.render(
            {"presupuesto": request.POST["presupuesto"], "datos": datos, "total": total, "orden":nueva_orden_compra}
        )
        pdf_file = HTML(string=html).write_pdf()
        file_object = BytesIO(pdf_file)

        nombre = 'OrdenCompra-{}.pdf'.format(datetime.now())

        nueva_orden_compra.archivo.save(nombre ,file_object)

        proveedores = Proveedor.objects.all()
        return render(request, "ordencompra.html", {"proveedores": proveedores})


def añadir_proveedor(request):
    if request.method == "GET":
        return render(request, "añadir_proveedor.html")
    else:
        try:
            nuevo_proveedor = Proveedor.objects.create(
                nombre=request.POST["nombre"],
                direccion=request.POST["direccion"],
                numero_telefono=request.POST["telefono"],
            )
            nuevo_proveedor.save()
            status = "Proveedor Creado Satisfactoriamente"
            return render(request, "añadir_proveedor.html", {"status": status})
        except:
            status = "Ha ocurrido un error"
            return render(request, "añadir_proveedor.html", {"status": status})
