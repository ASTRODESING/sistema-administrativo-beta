from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

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
            return render(request, "login_form.html", {"error": "Ha ocurrido un error, por favor inténtelo nuevamente"})
        else:
            login(request, user)
            return redirect('dashboard')


def inicio(request):
    return render(request, "inicio.html")

@login_required
def dashboard(request):
    return render(request, "dashboard.html")

@login_required
def logout_sesion(request):
    logout(request)
    return redirect('home')

def LoginPerso(LoginView):
    template_name="login_form.html"
