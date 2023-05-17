from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Categoria


# Create your views here.
def Inventario(request):
    categorias = Categoria.objects.all()
    productos = Producto.objects.all()

    if request.method == "GET":
        return render(request, "inventario.html", {"productos": productos, "categorias":categorias})
    
    else:
        try:
            prod = Producto.objects.create(
                codigo_de_barras = request.POST["codigo_de_barras"],
                nombre=request.POST["nombre"],
                descripcion=request.POST["descripcion"],
                categoria=Categoria.objects.get(nombre=request.POST["categoria"]),
                precio_venta=request.POST["precio_venta"],
                precio_compra=request.POST["precio_compra"],
                exento_de_impuesto=request.POST["excento"],
                stock=int(request.POST["stock"]),
            )
            prod.save()

            producto = Producto.objects.get(nombre=request.POST["nombre"])
            stock_actual = producto.stock
            producto.cantidad_comprada += stock_actual
            producto.save()
            sucess = "Guardado con Exito"
            return render(
                request, "inventario.html", {"status": sucess, "productos": productos,  "categorias":categorias}
            )
        except :
            error= 'Ha ocurrido un error intente de nuevo'
            return render(
                 request, "inventario.html", {"status": error, "productos": productos,  "categorias":categorias}
             )
        

def EditarProducto(request, producto_id):
    categorias = Categoria.objects.all()
    producto = get_object_or_404(Producto, pk=producto_id)

    if request.method == 'GET':
        return render(request, 'editproduct.html', {'producto':producto, 'categorias':categorias})
    else:
        try:
            producto.nombre = request.POST['nombre']
            producto.descripcion = request.POST['descripcion']
            producto.categoria = Categoria.objects.get(nombre=request.POST["categoria"])
            producto.precio_venta = request.POST['precio_venta']
            producto.precio_compra = request.POST['precio_compra']
            producto.exento_de_impuesto = request.POST['excento']
            producto.stock = request.POST['stock']
            producto.codigo_de_barras = request.POST['codigo_de_barras']
            suma = int(producto.stock) + int(request.POST['stock'])
            producto.cantidad_comprada = str(suma)
            producto.save()
            status = 'Producto Editado Satisfacoriamente'
            return render(request, 'editproduct.html', {'producto':producto,    'categorias':categorias, 'status':status})
        
        except:
            status = 'La Edicion del Producto ha Fallado, intente de nuevo'
            return render(request, 'editproduct.html', {'producto':producto,    'categorias':categorias, 'status':status})
        
def ElimnarProd(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    producto.delete()
    return redirect('inventario')

def Categorias(request):
    if request.method == 'GET':
        return render(request, 'categorias.html')
    else:
        destacado = request.POST['destacado'] if 'destacado' in request.POST else None
        try:

            if destacado is not None:
                cat = Categoria.objects.create(
                   nombre=request.POST["nombre"],
                   destacado = True
                )
                cat.save()
                status = 'Guardado con exito'
                return render(request, 'categorias.html', {'status':status})
            else:
                cat = Categoria.objects.create(
                   nombre=request.POST["nombre"],
                   destacado = False
                )
                cat.save()
                status = 'Guardado con exito'
                return render(request, 'categorias.html', {'status':status})
        except:
            status = 'Ha ocurrido un error, porfavor intente de nuevo'
            return render(request, 'categorias.html', {'status':status})
