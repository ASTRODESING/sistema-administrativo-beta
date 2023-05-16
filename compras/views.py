from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.template.loader import get_template
from .models import OrdenDeCompra, Proveedor
from io import BytesIO
from weasyprint import HTML
from datetime import datetime
import os

# Create your views here.
def panel(request):
    return render(request, "panel-compras.html")


def orden_compras(request):
    if request.method == "GET":
        proveedores = Proveedor.objects.all()
        return render(request, "ordencompra.html", {"proveedores": proveedores})
    else:
        datos = []
        datos_generales = {}
        nombres = request.POST.getlist("nombre_producto")
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

        dinero_restante = int(request.POST["presupuesto"]) - subtotal_productos
        template = get_template("pdf_ordencompra.html")
        datos_generales["fecha_actual"]= datetime.now()
        datos_generales["nombre_proveedor"]= Proveedor.objects.get(pk=request.POST["proveedor_id"]).nombre
        datos_generales["numero_telefono"]= Proveedor.objects.get(pk=request.POST["proveedor_id"]).numero_telefono
        datos_generales["monto"]= subtotal_productos
        datos_generales["presupuesto"]= request.POST["presupuesto"]



        nueva_orden_compra = OrdenDeCompra.objects.create(
        proveedor = Proveedor.objects.get(pk=request.POST["proveedor_id"]),
        monto =  subtotal_productos
        )
        nueva_orden_compra.save()


        html = template.render(
            {"datos": datos, "orden":nueva_orden_compra,"datos_generales":datos_generales}
        )
        pdf_file = HTML(string=html).write_pdf()
        file_object = BytesIO(pdf_file)

        nombre = 'OrdenCompra-{}.pdf'.format(datetime.now())

        nueva_orden_compra.archivo.save(nombre ,file_object)

        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="{}"'.format(nombre)
        return response


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
        
def historico_ordenes_compra(request):
    orden = OrdenDeCompra.objects.all()
    return render(request, "historico_ordenes_compra.html", {"ordenes":orden})

def get_pdf_orden(request, numero_orden):
    orden = get_object_or_404(OrdenDeCompra, pk=numero_orden)
    pdf = orden.archivo

    nombre = os.path.splitext(os.path.basename(pdf.name))[0]
    
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="{}.pdf"'.format(nombre)
    return response

def delete_ordenes_compra(request, numero_orden):
    orden = get_object_or_404(OrdenDeCompra, pk=numero_orden)
    orden.delete()
    return redirect("get_orden")

