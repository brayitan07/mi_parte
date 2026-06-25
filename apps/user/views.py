from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from apps.docente.models import Estudiante, Docente, Tarea, Curso, Materia
from apps.tareas.models import Tareas
from django.shortcuts import get_object_or_404
from django.contrib import messages


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

@staff_member_required
def panel_admin(request):
    total_estudiantes  = Estudiante.objects.count()
    total_docentes     = Docente.objects.count()
    total_tareas       = Tarea.objects.count()
    total_cursos       = Curso.objects.count()
    total_materias     = Materia.objects.count()
    usuarios_recientes = User.objects.select_related('role').order_by('-date_joined')[:5]

    return render(request, 'admin_panel/dashboard.html', {
        'total_estudiantes':  total_estudiantes,
        'total_docentes':     total_docentes,
        'total_tareas':       total_tareas,
        'total_cursos':       total_cursos,
        'total_materias':     total_materias,
        'usuarios_recientes': usuarios_recientes,
    })


# ── USUARIOS ──────────────────────────────────────────────────────────────────

@staff_member_required
def admin_usuarios(request):
    usuarios = User.objects.select_related('role').order_by('-date_joined')
    roles    = Role.objects.all()
    return render(request, 'admin_panel/usuarios.html', {
        'usuarios': usuarios,
        'roles':    roles,
    })


@staff_member_required
def admin_crear_usuario(request):
    roles = Role.objects.all()
    if request.method == 'POST':
        username  = request.POST.get('username', '').strip()
        email     = request.POST.get('email', '').strip()
        nombre    = request.POST.get('nombre', '').strip()
        password  = request.POST.get('password', '').strip()
        role_id   = request.POST.get('role')

        if not (username and password):
            return render(request, 'admin_panel/usuario_form.html', {
                'roles': roles,
                'error': 'Usuario y contraseña son obligatorios.',
                'form':  request.POST,
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'admin_panel/usuario_form.html', {
                'roles': roles,
                'error': f'El usuario "{username}" ya existe.',
                'form':  request.POST,
            })

        user = User(username=username, email=email, nombre=nombre)
        user.set_password(password)
        if role_id:
            user.role = get_object_or_404(Role, id=role_id)
        user.save()
        return redirect('admin_usuarios')

    return render(request, 'admin_panel/usuario_form.html', {
        'roles': roles,
        'accion': 'Crear',
    })


@staff_member_required
def admin_editar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    roles   = Role.objects.all()

    if request.method == 'POST':
        usuario.email  = request.POST.get('email',  usuario.email).strip()
        usuario.nombre = request.POST.get('nombre', usuario.nombre).strip()
        role_id        = request.POST.get('role')
        password       = request.POST.get('password', '').strip()

        if role_id:
            usuario.role = get_object_or_404(Role, id=role_id)
        else:
            usuario.role = None

        if password:
            usuario.set_password(password)

        usuario.save()
        return redirect('admin_usuarios')

    return render(request, 'admin_panel/usuario_form.html', {
        'roles':   roles,
        'usuario': usuario,
        'accion':  'Editar',
    })


@staff_member_required
def admin_eliminar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    if not usuario.is_superuser:
        usuario.delete()
    return redirect('admin_usuarios')


@staff_member_required
def admin_toggle_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    if not usuario.is_superuser:
        usuario.is_active = not usuario.is_active
        usuario.save()
    return redirect('admin_usuarios')


@staff_member_required
def admin_asignar_rol(request, user_id):
    """Asigna rol a un usuario vía POST (usado desde la tabla sin recargar)."""
    if request.method == 'POST':
        usuario = get_object_or_404(User, id=user_id)
        role_id = request.POST.get('role')
        if role_id:
            usuario.role = get_object_or_404(Role, id=role_id)
        else:
            usuario.role = None
        usuario.save()
    return redirect('admin_usuarios')


# ── ESTUDIANTES ───────────────────────────────────────────────────────────────

@staff_member_required
def admin_estudiantes(request):
    estudiantes = Estudiante.objects.select_related('curso', 'usuario').order_by('nombre')
    cursos      = Curso.objects.all()
    return render(request, 'admin_panel/estudiantes.html', {
        'estudiantes': estudiantes,
        'cursos':      cursos,
    })


@staff_member_required
def admin_crear_estudiante(request):
    cursos   = Curso.objects.all()
    usuarios = User.objects.filter(estudiante__isnull=True).order_by('username')
    if request.method == 'POST':
        nombre     = request.POST.get('nombre', '').strip()
        correo     = request.POST.get('correo', '').strip()
        curso_id   = request.POST.get('curso')
        usuario_id = request.POST.get('usuario')

        if not (nombre and correo and curso_id):
            return render(request, 'admin_panel/estudiante_form.html', {
                'cursos': cursos, 'usuarios': usuarios,
                'error': 'Nombre, correo y curso son obligatorios.',
                'form':  request.POST,
            })

        est = Estudiante(
            nombre = nombre,
            correo = correo,
            curso  = get_object_or_404(Curso, id=curso_id),
        )
        if usuario_id:
            est.usuario = get_object_or_404(User, id=usuario_id)
        est.save()
        return redirect('admin_estudiantes')

    return render(request, 'admin_panel/estudiante_form.html', {
        'cursos': cursos, 'usuarios': usuarios, 'accion': 'Crear',
    })


@staff_member_required
def admin_editar_estudiante(request, est_id):
    estudiante = get_object_or_404(Estudiante, id=est_id)
    cursos     = Curso.objects.all()
    usuarios   = User.objects.filter(
        estudiante__isnull=True
    ).order_by('username') | User.objects.filter(estudiante=estudiante)

    if request.method == 'POST':
        estudiante.nombre  = request.POST.get('nombre',  estudiante.nombre).strip()
        estudiante.correo  = request.POST.get('correo',  estudiante.correo).strip()
        curso_id           = request.POST.get('curso')
        usuario_id         = request.POST.get('usuario')

        if curso_id:
            estudiante.curso = get_object_or_404(Curso, id=curso_id)
        if usuario_id:
            estudiante.usuario = get_object_or_404(User, id=usuario_id)
        else:
            estudiante.usuario = None

        estudiante.save()
        return redirect('admin_estudiantes')

    return render(request, 'admin_panel/estudiante_form.html', {
        'cursos': cursos, 'usuarios': usuarios,
        'estudiante': estudiante, 'accion': 'Editar',
    })


@staff_member_required
def admin_eliminar_estudiante(request, est_id):
    estudiante = get_object_or_404(Estudiante, id=est_id)
    estudiante.delete()
    return redirect('admin_estudiantes')


# ── DOCENTES ──────────────────────────────────────────────────────────────────

@staff_member_required
def admin_docentes(request):
    docentes = (
        Docente.objects
        .select_related('usuario')
        .prefetch_related('asignaciones__materia', 'asignaciones__curso')
        .order_by('nombre')
    )
    return render(request, 'admin_panel/docentes.html', {'docentes': docentes})


@staff_member_required
def admin_crear_docente(request):
    usuarios = User.objects.filter(docente__isnull=True).order_by('username')
    if request.method == 'POST':
        nombre     = request.POST.get('nombre', '').strip()
        correo     = request.POST.get('correo', '').strip()
        telefono   = request.POST.get('telefono', '').strip()
        usuario_id = request.POST.get('usuario')

        if not (nombre and correo):
            return render(request, 'admin_panel/docente_form.html', {
                'usuarios': usuarios,
                'error': 'Nombre y correo son obligatorios.',
                'form':  request.POST,
            })

        doc = Docente(nombre=nombre, correo=correo, telefono=telefono)
        if usuario_id:
            doc.usuario = get_object_or_404(User, id=usuario_id)
        doc.save()
        return redirect('admin_docentes')

    return render(request, 'admin_panel/docente_form.html', {
        'usuarios': usuarios, 'accion': 'Crear',
    })


@staff_member_required
def admin_editar_docente(request, doc_id):
    docente  = get_object_or_404(Docente, id=doc_id)
    usuarios = User.objects.filter(
        docente__isnull=True
    ).order_by('username') | User.objects.filter(docente=docente)

    if request.method == 'POST':
        docente.nombre   = request.POST.get('nombre',   docente.nombre).strip()
        docente.correo   = request.POST.get('correo',   docente.correo).strip()
        docente.telefono = request.POST.get('telefono', docente.telefono).strip()
        usuario_id       = request.POST.get('usuario')

        if usuario_id:
            docente.usuario = get_object_or_404(User, id=usuario_id)
        else:
            docente.usuario = None

        docente.save()
        return redirect('admin_docentes')

    return render(request, 'admin_panel/docente_form.html', {
        'usuarios': usuarios, 'docente': docente, 'accion': 'Editar',
    })


@staff_member_required
def admin_eliminar_docente(request, doc_id):
    docente = get_object_or_404(Docente, id=doc_id)
    docente.delete()
    return redirect('admin_docentes')


# ── TAREAS ────────────────────────────────────────────────────────────────────

@staff_member_required
def admin_tareas(request):
    tareas = Tarea.objects.select_related(
        'asignacion__docente',
        'asignacion__materia',
        'asignacion__curso',
    ).order_by('-fecha_limite')
    return render(request, 'admin_panel/tareas.html', {'tareas': tareas})


@staff_member_required
def admin_eliminar_tarea_admin(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id)
    tarea.delete()
    return redirect('admin_tareas')