from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.http import HttpResponseNotFound
from django.template.loader import get_template
from .models import OrdenDeCompra, Perdida, Proveedor
from io import BytesIO
from weasyprint import HTML
from datetime import datetime
import os
from django.contrib.auth.decorators import login_required
from datetime import date


@login_required
def panel(request):
    return render(request, "panel-compras.html")

@login_required
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

        template = get_template("pdf_ordencompra.html")
        datos_generales["fecha_actual"] = datetime.now()
        datos_generales["nombre_proveedor"] = Proveedor.objects.get(
            pk=request.POST["proveedor_id"]
        ).nombre
        datos_generales["numero_telefono"] = Proveedor.objects.get(
            pk=request.POST["proveedor_id"]
        ).numero_telefono
        datos_generales["monto"] = subtotal_productos
        datos_generales["presupuesto"] = request.POST["presupuesto"]

        nueva_orden_compra = OrdenDeCompra.objects.create(
            proveedor=Proveedor.objects.get(pk=request.POST["proveedor_id"]),
            monto=subtotal_productos,
        )
        nueva_orden_compra.save()

        try:
            nueva_perdida =  Perdida.objects.get(año=date.today().year,mes=date.today().month,dia=date.today().day)
            nueva_perdida.perdida = datos_generales["monto"]
        except:
            nueva_perdida = Perdida.objects.create(
                perdida=datos_generales["monto"]
            )

        html = template.render(
            {
                "datos": datos,
                "orden": nueva_orden_compra,
                "datos_generales": datos_generales,
            }
        )
        pdf_file = HTML(string=html).write_pdf()
        file_object = BytesIO(pdf_file)

        nombre = "OrdenCompra-{}.pdf".format(datetime.now())

        nueva_orden_compra.archivo.save(nombre, file_object)

        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="{}"'.format(nombre)
        return response

@login_required
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

@login_required
def historico_ordenes_compra(request):
    orden = OrdenDeCompra.objects.all()
    return render(request, "historico_ordenes_compra.html", {"ordenes": orden})

@login_required
def get_pdf_orden(request, numero_orden):
    try:
        orden = get_object_or_404(OrdenDeCompra, pk=numero_orden)
        pdf = orden.archivo

        nombre = os.path.splitext(os.path.basename(pdf.name))[0]

        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="{}.pdf"'.format(nombre)
        return response
    except:
        return HttpResponseNotFound(
            "<h1>Archivo no encontrado o se encuentra en otra dirección</h1>"
        )

@login_required
def delete_ordenes_compra(request, numero_orden):
    orden = get_object_or_404(OrdenDeCompra, pk=numero_orden)
    orden.delete()
    return redirect("get_orden")

@login_required
def proveedores(request):
    if request.method == "GET":
        get_proveedores = Proveedor.objects.all()
        return render(request, "proveedores.html", {"proveedores": get_proveedores})
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
            status = "A ocurrido un error"
            return render(request, "añadir_proveedor.html", {"status": status})

@login_required
def editar_proveedores(request, id_proveedor):
    get_proveedor = Proveedor.objects.get(pk=id_proveedor)
    if request.method =='GET':
        return render(request, 'editproveedor.html', {'proveedor':get_proveedor})
    else:
        try: 
            get_proveedor.nombre = request.POST['nombre']
            get_proveedor.direccion = request.POST['direccion']
            get_proveedor.numero_telefono = request.POST['telefono']
            get_proveedor.save()
            status = "Editado Satisfactoriamente"
            return render(request, 'editproveedor.html', {'proveedor':get_proveedor,'status':status})
        except:
            status = "A ocurrido un error"
            return render(request, 'editproveedor.html', {'proveedor':get_proveedor, 'status':status})

@login_required
def eliminar_proveedores(request, id_proveedor):
    proveedor_eliminar = Proveedor.objects.get(pk=id_proveedor)
    proveedor_eliminar.delete()
    return redirect("proveedores")
