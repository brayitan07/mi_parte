from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from apps.docente.models import Estudiante, Docente, Tarea, Curso, Materia
from apps.tareas.models import Tareas


from .forms import UserForm
from .models import Role
from .models import User


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

# ========= PÁGINAS PÚBLICAS =========

def prescolar(request):
    return render(request, 'prescolar.html')

def primaria(request):
    return render(request, 'primaria.html')

def segundaria(request):
    return render(request, 'segundaria.html')

def feria_ciencia(request):
    return render(request, 'feria-ciencia.html')

def festival_artistico(request):
    return render(request, 'festival-artistico.html')

def semana_lectura(request):
    return render(request, 'semana-lectura.html')

# ========= PANEL ADMINISTRADOR =========
@staff_member_required
def panel_admin(request):
    total_estudiantes = Estudiante.objects.count()
    total_docentes    = Docente.objects.count()
    total_tareas      = Tarea.objects.count()
    total_cursos      = Curso.objects.count()
    total_materias    = Materia.objects.count()
    usuarios_recientes = User.objects.order_by('-date_joined')[:5]

    return render(request, 'admin_panel/dashboard.html', {
        'total_estudiantes': total_estudiantes,
        'total_docentes':    total_docentes,
        'total_tareas':      total_tareas,
        'total_cursos':      total_cursos,
        'total_materias':    total_materias,
        'usuarios_recientes': usuarios_recientes,
    })

@staff_member_required
def admin_usuarios(request):
    usuarios = User.objects.select_related('role').order_by('-date_joined')
    return render(request, 'admin_panel/usuarios.html', {'usuarios': usuarios})

@staff_member_required
def admin_toggle_usuario(request, user_id):
    from django.shortcuts import get_object_or_404
    usuario = get_object_or_404(User, id=user_id)
    usuario.is_active = not usuario.is_active
    usuario.save()
    return redirect('admin_usuarios')

@staff_member_required
def admin_tareas(request):
    tareas = Tarea.objects.select_related(
        'asignacion__docente',
        'asignacion__materia',
        'asignacion__curso'
    ).order_by('-fecha_limite')
    return render(request, 'admin_panel/tareas.html', {'tareas': tareas})

@staff_member_required
def admin_estudiantes(request):
    estudiantes = Estudiante.objects.select_related('curso', 'usuario').order_by('nombre')
    return render(request, 'admin_panel/estudiantes.html', {'estudiantes': estudiantes})

@staff_member_required
def admin_docentes(request):
    docentes = Docente.objects.select_related('usuario').prefetch_related('asignaciones__materia', 'asignaciones__curso').order_by('nombre')
    return render(request, 'admin_panel/docentes.html', {'docentes': docentes})