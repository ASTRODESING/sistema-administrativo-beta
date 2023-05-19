from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from compras.models import OrdenDeCompra, Proveedor, Perdida
from items.models import Producto
from ventas.models import Cliente, Ganancias, NumeroDeClientes
from datetime import date


def login_sesion(request):
    if request.method == "GET":
        return render(request, "login_form.html")
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user == None:
            return render(
                request,
                "login_form.html",
                {"error": "Ha ocurrido un error, por favor inténtelo nuevamente"},
            )
        else:
            login(request, user)
            try:
                inicializacion = Ganancias.objects.get(año=date.today().year,mes=date.today().month,dia=date.today().day)
                return redirect("dashboard")
                
            except:
                ganacias_hoy = Ganancias.objects.create(
                    ganancia = 0
                )
                ganacias_hoy.save()
                perdidas_hoy = Perdida.objects.create(
                    perdida=0
                )
                perdidas_hoy.save()
                clientes_hoy = NumeroDeClientes.objects.create(
                    numero_clientes = 0
                )
                clientes_hoy.save()
                return redirect("dashboard")
            

            


def inicio(request):
    return render(request, "inicio.html")


@login_required
def dashboard(request):
    proveedores = Proveedor.objects.all()
    clientes = Cliente.objects.all()
    ordenes_de_compra = OrdenDeCompra.objects.all()
    productos = Producto.objects.all()

    return render(
        request,
        "dashboard.html",
        {
            "proveedores": proveedores,
            "clientes": clientes,
            "ordenesdecompra": ordenes_de_compra,
            "productos": productos
        },
    )


@login_required
def logout_sesion(request):
    logout(request)
    return redirect("home")


def LoginPerso(LoginView):
    template_name = "login_form.html"
