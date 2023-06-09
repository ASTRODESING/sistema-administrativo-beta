import os
from datetime import datetime 
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.template.loader import get_template
from items.models import Producto
from io import BytesIO
from weasyprint import HTML
from datetime import date
from ventas.models import Cliente, Factura, FormasDePago, Ganancias, NumeroDeClientes
from django.contrib.auth.decorators import login_required
from login.models import PrecioDolar, DatosEmpresa

@login_required
def panel(request):
    return render(request, "panel-ventas.html")

@login_required
def caja(request):
    if request.method == "GET":
        productos = Producto.objects.all()
        clientes = Cliente.objects.all()
        formas_de_pago = FormasDePago.objects.all()
        precio_dolar = PrecioDolar.objects.all().first

        return render(
            request,
            "caja.html",
            {
                "productos": productos,
                "clientes": clientes,
                "formas_de_pagos": formas_de_pago,
                "precio_dolar": precio_dolar
            },
        )
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

@login_required
def imprimir_pdf(request):
    precio_dolar = PrecioDolar.objects.all().first()
    datos_empresa = DatosEmpresa.objects.all().first()
    contenido = []
    total = {}
    datos = {}
    productos_lista = request.POST
    contador = 0

    total["total_excento"] = 0
    total["total_sin_excento"] = 0

    for p in productos_lista.getlist("producto"):
        producto_stock = productos_lista.getlist("stock")

        producto = Producto.objects.get(nombre=p)
        subtotal_raw = (float(producto.precio_venta) * float(producto_stock[contador])) * precio_dolar.precio

        contenido.append(
            {
                "nombre": p,
                "precio": float(producto.precio_venta) * precio_dolar.precio,
                "cantidad": producto_stock[contador],
                "subtotal": subtotal_raw,
                "excento": producto.exento_de_impuesto,
            }
        )
        if contenido[contador]["excento"]:
            total["total_excento"] += contenido[contador]["subtotal"]
        else:
            total["total_sin_excento"] += contenido[contador]["subtotal"]

        contador += 1

    total["iva"] = total["total_sin_excento"] * 0.16
    print(total["total_sin_excento"])
    print(total["iva"])
    total["subtotal_sin_excento_con_iva"] = total["total_sin_excento"] + total["iva"]

    print(total["subtotal_sin_excento_con_iva"])
    
    total["total"] = round((total["subtotal_sin_excento_con_iva"] + total["total_excento"]),3) 
    print(total["total"])

    datos["fecha"] = date.today
    datos["cliente"] = request.POST["cliente"]
    datos["forma_de_pago"] = request.POST["forma_de_pago"]
    datos["usuario"] = request.user.username
    datos["referencia"] = request.POST["referencia"]

    try:
        nueva_factura = Factura.objects.create(
            id_cliente=  Cliente.objects.get(nombre=request.POST["cliente"]),
            monto = total["total"],
            usuario = request.user.username,
            forma_de_pago = FormasDePago.objects.get(forma=request.POST["forma_de_pago"]),
            referencia = request.POST["referencia"]

        )
    except:
        nueva_factura = Factura.objects.create(
            id_cliente=  Cliente.objects.get(nombre=request.POST["cliente"]),
            monto = total["total"],
            usuario = request.user.username,
            forma_de_pago = FormasDePago.objects.get(forma=request.POST["forma_de_pago"]),
            referencia = 0

        )

    try:
        actualizar_ganancias = Ganancias.objects.get(año=date.today().year,mes=date.today().month,dia=date.today().day) 
        actualizar_ganancias.ganancia += total["total"]
        actualizar_ganancias.save()

        actualizar_numero_clientes = NumeroDeClientes.objects.get(año=date.today().year,mes=date.today().month,dia=date.today().day)
        actualizar_numero_clientes.numero_clientes += 1
    except:
        actualizar_ganancias = Ganancias.objects.create(
            ganancia= total["total"]
        )
        actualizar_numero_clientes = NumeroDeClientes.objects.create(
            numero_clientes = 1
        )
    

    nueva_factura.save()

    datos["numero_factura"] = nueva_factura.numero_factura

    template = get_template("pdf.html")
    html = template.render({"contenido": contenido, "total": total, "datos": datos, "datos_empresa":datos_empresa})
    pdf_file = HTML(string=html).write_pdf()
    file_object = BytesIO(pdf_file)

    nombre = 'factura-{}.pdf'.format(datetime.now())
    
    nueva_factura.documento.save(nombre ,file_object)

    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="{}"'.format(nombre)
    return response


@login_required
def get_factura(request, numero_factur):
    try:
        objeto = get_object_or_404(Factura, numero_factura=numero_factur)
        pdf_file = objeto.documento

        nombre = os.path.splitext(os.path.basename(pdf_file.name))[0]

        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="{}.pdf"'.format(nombre)
        return response
    except:
        return HttpResponseNotFound('<h1>Archivo no encontrado o se encuentra en otra dirección</h1>')

@login_required
def get_productos(request, id_producto):
    productos = Producto.objects.get(id=id_producto)
    data = {
        "id": productos.pk,
        "nombre": productos.nombre,
        "precio": productos.precio_venta,
        "excento": productos.exento_de_impuesto
    }
    return JsonResponse(data)

@login_required
def facturas(request):
    facturas = Factura.objects.all()
    return render(request, "facturas.html", {"facturas":facturas})

@login_required
def clientes(request):
    if request.method == 'GET':
        clientes = Cliente.objects.all()
        return render(request, "clientes.html", {"clientes":clientes})
    else:
        try:
            clientes = Cliente.objects.all()
            status = 'Cliente Creado Satisfactoriamente'
            nuevo_cliente = Cliente.objects.create(
                nombre = request.POST["nombre"],
                ci_rif = request.POST["cidrif"]
            )
            nuevo_cliente.save()
            return render(request, "clientes.html", {'status':status, "clientes":clientes})
        except:
            clientes = Cliente.objects.all()
            status = 'Ha Ocurrido un Error Intente de Nuevo'
            return render(request, "clientes.html",  {'status':status, "clientes":clientes})

@login_required
def nuevo_cliente(request):
    if request.method == "GET":
        return render(request, "nuevocliente.html")
    else:
        try:
            status = 'Cliente Creado Satisfactoriamente'
            nuevo_cliente = Cliente.objects.create(
                nombre = request.POST["nombre"],
                ci_rif = request.POST["cidrif"]
            )
            nuevo_cliente.save()
            return render(request, "nuevocliente.html", {'status':status})
        except:
             status = 'Ha Ocurrido un Error Intente de Nuevo'
             return render(request, "nuevocliente.html",  {'status':status})


@login_required
def elimnar_cliente(request, id_cliente):
    cliente = get_object_or_404(Cliente, pk=id_cliente)
    cliente.delete()
    return redirect('clientes')


@login_required
def edit_cliente(request, id_cliente):
    cliente = get_object_or_404(Cliente, pk=id_cliente)

    if request.method == 'GET':
        return render(request, 'editcliente.html', {"clientes":cliente})
    else:
        try:
            cliente.nombre = request.POST['nombre']
            cliente.ci_rif = request.POST['cidrif']
            cliente.save()
            status = 'Cliente Editado Satisfacoriamente'
            return render(request, 'editcliente.html', {"clientes":cliente, "status":status})
        
        except:
            status = 'La Edicion del Cliente ha Fallado, intente de nuevo'
            return render(request, 'editcliente.html', {"clientes":cliente, "status":status})
        