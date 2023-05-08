from django.shortcuts import render, HttpResponse

# Create your views here.
def Panel(request):
    return render(request,"panel-compras.html")