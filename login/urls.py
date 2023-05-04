from django.urls import path, include
from . import views
from .views import LoginPerso

urlpatterns = [
    path('', views.login_sesion, name="login"),
    path('login/', views.login_sesion, name="login"),
    path('inicio/', views.inicio, name='home'),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('logout/', views.logout_sesion, name="logout"),
    path('login/', LoginPerso),
    path("items/", include('items.urls')),
]