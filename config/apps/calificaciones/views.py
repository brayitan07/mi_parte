from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Docente, Estudiante, Materia, Curso, Calificacion, Tarea, Asistencia, Mensaje
from datetime import datetime

DOCENTE_ID = 1

def get_docente():
    return Docente.objects.filter(id=DOCENTE_ID).first()

# ── DASHBOARD ──────────────────────────────────────────────
def dashboard_docente(request):
    docente = get_docente()
    if not docente:
        return render(request, 'dashboard_docente.html', {})
    cursos = docente.cursos.all()
    total_estudiantes = Estudiante.objects.filter(curso__in=cursos).count()
    total_tareas = Tarea.objects.filter(docente=docente).count()
    calificaciones = Calificacion.objects.filter(docente=docente)
    promedio = round(sum(c.promedio for c in calificaciones) / calificaciones.count(), 1) if calificaciones.exists() else 0
    context = {
        'docente': docente,
        'cursos': cursos,
        'total_estudiantes': total_estudiantes,
        'total_tareas': total_tareas,
        'promedio': promedio,
        'tareas_recientes': Tarea.objects.filter(docente=docente).order_by('-fecha_limite')[:3],
    }
    return render(request, 'dashboard_docente.html', context)

# ── CURSOS ──────────────────────────────────────────────
def cursos_docente(request):
    docente = get_docente()
    cursos = docente.cursos.all() if docente else []
    context = {
        'docente': docente,
        'cursos': cursos,
        'total_estudiantes': Estudiante.objects.filter(curso__in=cursos).count() if docente else 0,
        'total_materias': docente.materias.count() if docente else 0,
    }
    return render(request, 'cursos_docente.html', context)

# ── TAREAS ──────────────────────────────────────────────
def tarea_docente(request):
    docente = get_docente()
    tareas = Tarea.objects.filter(docente=docente) if docente else []
    cursos = docente.cursos.all() if docente else []
    materias = docente.materias.all() if docente else []
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion', '')
        materia_id = request.POST.get('materia')
        curso_id = request.POST.get('curso')
        fecha_limite = request.POST.get('fecha_limite')
        if titulo and materia_id and curso_id and fecha_limite:
            Tarea.objects.create(
                titulo=titulo, descripcion=descripcion,
                materia_id=materia_id, curso_id=curso_id,
                docente=docente, fecha_limite=fecha_limite,
                estado='pendiente'
            )
        return redirect('tarea_docente')
    context = {
        'docente': docente, 'tareas': tareas, 'cursos': cursos, 'materias': materias,
        'pendientes': tareas.filter(estado='pendiente').count() if hasattr(tareas, 'filter') else 0,
        'entregadas': tareas.filter(estado='entregada').count() if hasattr(tareas, 'filter') else 0,
        'total_tareas': tareas.count() if hasattr(tareas, 'count') else 0,
    }
    return render(request, 'tarea_docente.html', context)

def eliminar_tarea(request, id):
    tarea = get_object_or_404(Tarea, id=id)
    tarea.delete()
    return redirect('tarea_docente')

# ── CALIFICACIONES ──────────────────────────────────────────────
def calificaciones_docente(request):
    docente = get_docente()
    cursos = docente.cursos.all() if docente else []
    materias = docente.materias.all() if docente else []
    curso_id = request.GET.get('curso')
    materia_id = request.GET.get('materia')
    curso_sel = None
    materia_sel = None
    estudiantes = []
    calificaciones_map = {}
    if curso_id and materia_id:
        curso_sel = get_object_or_404(Curso, id=curso_id)
        materia_sel = get_object_or_404(Materia, id=materia_id)
        estudiantes = Estudiante.objects.filter(curso=curso_sel)
        for est in estudiantes:
            cal = Calificacion.objects.filter(estudiante=est, materia=materia_sel, docente=docente).first()
            calificaciones_map[est.id] = cal
    total_cals = Calificacion.objects.filter(docente=docente)
    promedio_general = round(sum(c.promedio for c in total_cals) / total_cals.count(), 1) if total_cals.exists() else 0
    context = {
        'docente': docente, 'cursos': cursos, 'materias': materias,
        'curso_sel': curso_sel, 'materia_sel': materia_sel,
        'estudiantes': estudiantes, 'calificaciones_map': calificaciones_map,
        'promedio_general': promedio_general,
        'en_riesgo': sum(1 for c in total_cals if c.promedio < 3.0),
        'destacados': sum(1 for c in total_cals if c.promedio >= 4.5),
        'total_notas': total_cals.count(),
    }
    return render(request, 'calificaciones_docente.html', context)

def guardar_todas_calificaciones(request):
    if request.method == 'POST':
        docente = get_docente()
        materia_id = request.POST.get('materia_id')
        curso_id = request.POST.get('curso_id')
        estudiantes = Estudiante.objects.filter(curso_id=curso_id)
        for est in estudiantes:
            tarea = request.POST.get(f'tarea_{est.id}', 0)
            parcial = request.POST.get(f'parcial_{est.id}', 0)
            examen = request.POST.get(f'examen_{est.id}', 0)
            Calificacion.objects.update_or_create(
                estudiante=est, materia_id=materia_id, docente=docente,
                defaults={'tarea': tarea, 'parcial': parcial, 'examen': examen}
            )
        return redirect(f'/docente/calificaciones/?curso={curso_id}&materia={materia_id}')
    return redirect('calificaciones_docente')

# ── ASISTENCIA ──────────────────────────────────────────────
def asistencia_docente(request):
    docente = get_docente()
    cursos = docente.cursos.all() if docente else []
    curso_id = request.GET.get('curso')
    curso_sel = None
    estudiantes = []
    if curso_id:
        curso_sel = get_object_or_404(Curso, id=curso_id)
        estudiantes = Estudiante.objects.filter(curso=curso_sel)
    if request.method == 'POST':
        curso_id_post = request.POST.get('curso_id')
        fecha_str = request.POST.get('fecha')
        try:
            fecha = datetime.strptime(fecha_str, '%B %d, %Y').date()
        except:
            fecha = timezone.now().date()
        for est in Estudiante.objects.filter(curso_id=curso_id_post):
            estado = request.POST.get(f'estado_{est.id}', 'presente')
            Asistencia.objects.update_or_create(estudiante=est, fecha=fecha, defaults={'estado': estado})
        return redirect(f'/docente/asistencia/?curso={curso_id_post}')
    asistencias_map = {}
    for est in estudiantes:
        asis = Asistencia.objects.filter(estudiante=est, fecha=timezone.now().date()).first()
        asistencias_map[est.id] = asis.estado if asis else 'presente'
    context = {
        'docente': docente, 'cursos': cursos, 'curso_sel': curso_sel,
        'estudiantes': estudiantes, 'asistencias_map': asistencias_map,
        'fecha_hoy': timezone.now().date(),
        'presentes': sum(1 for v in asistencias_map.values() if v == 'presente'),
        'ausentes': sum(1 for v in asistencias_map.values() if v == 'ausente'),
        'tardanzas': sum(1 for v in asistencias_map.values() if v == 'tardanza'),
        'total': len(estudiantes),
    }
    return render(request, 'asistencia_docente.html', context)

# ── MENSAJES ──────────────────────────────────────────────
def mensajes_docente(request):
    docente = get_docente()
    estudiantes = Estudiante.objects.filter(curso__in=docente.cursos.all()) if docente else []
    estudiante_id = request.GET.get('estudiante')
    estudiante_sel = None
    mensajes = []
    if estudiante_id:
        estudiante_sel = get_object_or_404(Estudiante, id=estudiante_id)
        mensajes = Mensaje.objects.filter(docente=docente, estudiante=estudiante_sel)
        Mensaje.objects.filter(docente=docente, estudiante=estudiante_sel, enviado_por='estudiante').update(leido=True)
    if request.method == 'POST':
        contenido = request.POST.get('contenido')
        est_id = request.POST.get('estudiante_id')
        if contenido and est_id:
            Mensaje.objects.create(docente=docente, estudiante_id=est_id, contenido=contenido, enviado_por='docente')
        return redirect(f'/docente/mensajes/?estudiante={est_id}')
    sin_leer = Mensaje.objects.filter(docente=docente, enviado_por='estudiante', leido=False).count() if docente else 0
    context = {
        'docente': docente, 'estudiantes': estudiantes,
        'estudiante_sel': estudiante_sel, 'mensajes': mensajes,
        'sin_leer': sin_leer,
        'total_mensajes': Mensaje.objects.filter(docente=docente).count() if docente else 0,
    }
    return render(request, 'mensajes_docente.html', context)

# ── CONFIGURACION ──────────────────────────────────────────────
def configuracion_docente(request):
    docente = get_docente()
    if request.method == 'POST' and docente:
        docente.nombre = request.POST.get('nombre', docente.nombre)
        docente.correo = request.POST.get('correo', docente.correo)
        docente.telefono = request.POST.get('telefono', docente.telefono)
        docente.save()
    return render(request, 'configuracion_docente.html', {'docente': docente})