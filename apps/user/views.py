from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.


def registrar_usuario(request):
    if request.method == "POST":
        form = UserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            user.set_password(form.cleaned_data["password"])

            user.save()

            login(request, user)

            return redirect("index")

    else:
        form = UserForm()

    return render(request, "user/registrar_usuario.html", {"registroForm": form})


def iniciar_sesion(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect("index")
    else:
        form = AuthenticationForm()

    return render(request, "user/iniciar_sesion.html", {"form": form})


def cerrar_sesion(request):
    logout(request)
    return render(request, "user/index.html")


def inicio(request):
    return render(request, "user/inicio.html")
