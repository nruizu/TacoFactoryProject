#Autor: Nicolas Ruiz
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .form import RegistroForm, LoginForm
from django.http import HttpResponse


# Create your views here.

class HomeView(TemplateView):
    def get(self, request):
        if self.request.user.is_authenticated:
            return render(request, "home/index_loged.html")  # Plantilla para usuarios autenticados
        return render(request, "home/index.html")

def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión después del registro
            return redirect("home")  # Redirige a la página principal
        else:
            print(form.errors.as_data())
    else:
        form = RegistroForm()
    return render(request, "user/registro.html", {"form": form})

def iniciar_sesion(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            correo = form.cleaned_data["username"]
            contraseña = form.cleaned_data["password"]
            user = authenticate(request, email=correo, password=contraseña)
            if user is not None:
                login(request, user)
                return redirect("home")
        else:
            print(form.errors.as_data())
    else:
        form = LoginForm()
    return render(request, "user/login.html", {"form": form})

def cerrar_sesion(request):
    logout(request)
    return redirect("home")

def puntos_fisicos(request):
    return render(request, 'mapa/puntos_fisicos.html')