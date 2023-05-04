import os
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.template.loader import get_template
from items.models import Producto
from io import BytesIO
from weasyprint import HTML
from datetime import date



def Panel(request):
    return render(request, "panel-ventas.html")


def Caja(request):
    if request.method == "GET":
        productos = Producto.objects.all()
        return render(request, "caja.html", {"productos": productos})
    else:
        productos_lista = request.POST
        contador = 0
        productos = Producto.objects.all()

        for p in productos_lista.getlist("producto"):
            producto_stock = productos_lista.getlist("stock")

            producto_actualizar = Producto.objects.get(nombre=p)
            producto_actualizar.stock -= int(producto_stock[contador])
            producto_actualizar.cantidad_vendida += int(producto_stock[contador])

            producto_actualizar.save()
            contador += 1

        return imprimir_pdf(request)


def imprimir_pdf(request):
    
    contenido = []
    total = {}
    datos = {}
    productos_lista = request.POST
    contador = 0

    total['total_excento'] = 0
    total['total_sin_excento'] = 0

    for p in productos_lista.getlist("producto"):
        producto_stock = productos_lista.getlist("stock")

        producto = Producto.objects.get(nombre=p)
        subtotal_raw = float(producto.precio_venta) * float(producto_stock[contador])

        contenido.append(
            {
                "nombre": p,
                "precio": producto.precio_venta,
                "cantidad": producto_stock[contador],
                "subtotal": round(subtotal_raw,2),
                "excento": producto.execento_de_impuesto
            }
        )
        if contenido[contador]['excento']:
            total['total_excento'] += contenido[contador]['subtotal']
        else:
            total['total_sin_excento'] += contenido[contador]['subtotal']
        
        
        
        contador += 1
    

    total['iva'] = round(total['total_sin_excento']*0.16, 2)
    total['subtotal_sin_excento_con_iva'] = round(total['total_sin_excento'] +  total['iva'],2)
    total['total'] = total['subtotal_sin_excento_con_iva'] + total['total_excento']

    datos['fecha']= date.today

    template = get_template("pdf.html")
    html = template.render({"contenido": contenido, "total":total, 'datos':datos})
    pdf_file = HTML(string=html).write_pdf()

    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="report.pdf"'
    return response




def get_Productos(request, id_producto):
    productos = Producto.objects.get(id=id_producto)
    data = {
        "id": productos.pk,
        "nombre": productos.nombre,
        "precio": productos.precio_venta,
        "excento": productos.execento_de_impuesto
    }
    return JsonResponse(data)


def Reportes(request):
    return render(request, "caja.html")


def Clientes(request):
    return render(request, "caja.html")
