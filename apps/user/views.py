from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .forms import UserForm
from .models import Role


def registrar_usuario(request):

    if request.method == "POST":

        form = UserForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.set_password(
                form.cleaned_data["password"]
            )

            # Asignar rol Usuario por defecto
            rol_usuario = Role.objects.get(
                nombre__iexact="usuario"
            )

            user.role = rol_usuario

            user.save()

            return redirect("iniciar_sesion")

    else:

        form = UserForm()

    return render(
        request,
        "user/registrar_usuario.html",
        {"registroForm": form}
    )


def iniciar_sesion(request):

    if request.method == "POST":

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            if user.is_superuser:
                return redirect("panel_admin")

            if user.role:

                if user.role.nombre.lower() == "docente":
                    return redirect("dashboard_docente")
                
                elif user.role.nombre.lower() == "estudiante":
                    return redirect("dashboard_alumno")

                elif user.role.nombre.lower() == "usuario":
                    return redirect("panel_usuario")

            return redirect("panel_usuario")

    else:

        form = AuthenticationForm()

    return render(
        request,
        "user/iniciar_sesion.html",
        {"form": form}
    )


@login_required
def cerrar_sesion(request):

    logout(request)

    return redirect("iniciar_sesion")


def inicio(request):

    return render(
        request,
        "index.html"
    )


@login_required
def redireccion_usuario(request):

    if request.user.is_superuser:
        return redirect("panel_admin")

    if request.user.role:

        if request.user.role.nombre.lower() == "docente":
            return redirect("dashboard_docente")

        elif request.user.role.nombre.lower() == "estudiante":
            return redirect("dashboard_alumno")

        elif request.user.role.nombre.lower() == "usuario":
            return redirect("panel_usuario")

    return redirect("panel_usuario")


# ========= PANELES =========

@login_required
def panel_usuario(request):

    return render(
        request,
        "user/panel_usuario.html"
    )


@login_required
def panel_estudiante(request):

    return render(
        request,
        "user/inicio.html"
    )


@login_required
def panel_profesor(request):

    return redirect("dashboard_docente")


@login_required
def panel_admin(request):

    return redirect("admin:index")