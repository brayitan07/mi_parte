from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserForm


def registrar_usuario(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect("iniciar_sesion")
    else:
        form = UserForm()
    return render(request, "user/registrar_usuario.html", {"registroForm": form})


def iniciar_sesion(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # superusuario va directo al admin
            if user.is_superuser:
                return redirect("/admin/")

            # obtiene el nombre del rol desde la FK
            rol = getattr(user.role, 'nombre', '').lower() if user.role else ''

            if rol == 'docente':
                return redirect('dashboard_docente')
            elif rol == 'alumno':
                return redirect('dashboard_alumno')
            else:
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, "user/iniciar_sesion.html", {"form": form})


@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect("iniciar_sesion")


def inicio(request):
    return render(request, "index.html")