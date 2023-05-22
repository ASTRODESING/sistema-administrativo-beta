from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from compras.models import Perdida
from items.models import Producto
from ventas.models import Ganancias, NumeroDeClientes
from .models import PrecioDolar
from datetime import date
from django.db.models import Max, Sum

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
    producto_mas_vendido = Producto.objects.aggregate(Max('cantidad_vendida'))
    producto = Producto.objects.filter(cantidad_vendida = producto_mas_vendido['cantidad_vendida__max']).first()
    ganancias_mensual = Ganancias.objects.filter(mes=date.today().month).aggregate(Sum('ganancia'))
    perdida_mensual = Perdida.objects.filter(mes=date.today().month).aggregate(Sum('perdida'))
    clientes_mensual = NumeroDeClientes.objects.filter(mes=date.today().month).aggregate(Sum('numero_clientes'))
    precio_dolar = PrecioDolar.objects.all().first()

    if request.method == 'GET':
        return render(
            request,
            "dashboard.html",
            {
                'ganancia_mensual':ganancias_mensual['ganancia__sum'],
                'perdida_mensual': perdida_mensual['perdida__sum'],
                'cliente_mensual': clientes_mensual['numero_clientes__sum'],
                'producto_mas_vendido':producto,
                'precio_dolar':precio_dolar
            },
        )
    else:
        precio_dolar.precio = float(request.POST['preciodolar'])
        precio_dolar.save()
        return render(
            request,
            "dashboard.html",
            {
                'ganancia_mensual':ganancias_mensual['ganancia__sum'],
                'perdida_mensual': perdida_mensual['perdida__sum'],
                'cliente_mensual': clientes_mensual['numero_clientes__sum'],
                'producto_mas_vendido':producto,
                'precio_dolar':precio_dolar
            },
        )



@login_required
def logout_sesion(request):
    logout(request)
    return redirect("home")


def LoginPerso(LoginView):
    template_name = "login_form.html"
