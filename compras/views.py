from django.shortcuts import render, HttpResponse

# Create your views here.
def panel(request):
    return render(request,"panel-compras.html")

def orden_compras(request):
    return render(request,"ordencompra.html")