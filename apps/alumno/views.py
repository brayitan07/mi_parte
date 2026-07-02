
# apps/alumno/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

from apps.tareas.models import Tareas, RespuestaCorrecta, RespuestaEstudiante
from apps.docente.models import (
    Estudiante, Calificacion, Asistencia, Mensaje,
    Tarea, Docente, AsignacionDocente, PeriodoAcademico,
)


# ─────────────────────────────────────────
# UTILIDAD
# ─────────────────────────────────────────

def _get_estudiante(request):
    """Devuelve el Estudiante ligado al usuario autenticado."""
    try:
        return request.user.estudiante
    except Estudiante.DoesNotExist:
        return None


def _get_stats(estudiante):
    """Estadísticas generales del estudiante."""
    calificaciones = Calificacion.objects.filter(estudiante=estudiante)
    promedios = [c.promedio for c in calificaciones]
    promedio_general = round(sum(promedios) / len(promedios), 1) if promedios else 0

    asistencias   = Asistencia.objects.filter(estudiante=estudiante)
    total_asis    = asistencias.count()
    presentes     = asistencias.filter(estado='presente').count()
    tardanzas     = asistencias.filter(estado='tardanza').count()
    ausentes      = asistencias.filter(estado='ausente').count()
    porcentaje_asistencia = round((presentes / total_asis) * 100) if total_asis > 0 else 0

    aprobadas  = sum(1 for p in promedios if p >= 3.0)
    en_riesgo  = sum(1 for p in promedios if p < 3.0)
    total_logros = sum([
        porcentaje_asistencia >= 90,
        promedio_general >= 4.5,
        promedio_general >= 3.0,
    ])

    return {
        'calificaciones':      calificaciones,
        'promedio_general':    promedio_general,
        'porcentaje_asistencia': porcentaje_asistencia,
        'presentes':           presentes,
        'tardanzas':           tardanzas,
        'ausentes':            ausentes,
        'aprobadas':           aprobadas,
        'en_riesgo':           en_riesgo,
        'total_logros':        total_logros,
    }


# ─────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────

@login_required
def dashboard_alumno(request):
    estudiante = _get_estudiante(request)
    if not estudiante:
        return render(request, 'alumno/dashboard_alumno.html', {})

    stats    = _get_stats(estudiante)
    tareas   = Tarea.objects.filter(asignacion__curso=estudiante.curso)
    mensajes = Mensaje.objects.filter(estudiante=estudiante).order_by('-fecha')
    sin_leer = mensajes.filter(leido=False, enviado_por='docente').count()

    context = {
        'estudiante':        estudiante,
        'tareas_pendientes': tareas.filter(estado='pendiente').count(),
        'mensajes_recientes': mensajes[:3],
        'mensajes_sin_leer': sin_leer,
        **stats,
    }
    return render(request, 'alumno/dashboard_alumno.html', context)


# ─────────────────────────────────────────
# MATERIAS
# ─────────────────────────────────────────

@login_required
def materias_alumno(request):
    estudiante = _get_estudiante(request)
    if not estudiante:
        return render(request, 'alumno/materias_alumno.html', {})

    # Asignaciones del curso del estudiante con sus calificaciones
    asignaciones = AsignacionDocente.objects.filter(
        curso=estudiante.curso
    ).select_related('materia', 'docente')

    # Por cada asignación calcula el promedio general del estudiante
    materias_data = []
    for asig in asignaciones:
        cals = Calificacion.objects.filter(
            estudiante=estudiante, asignacion=asig
        )
        promedios = [c.promedio for c in cals]
        prom = round(sum(promedios) / len(promedios), 2) if promedios else None
        materias_data.append({
            'asignacion': asig,
            'promedio':   prom,
            'periodos':   cals.count(),
        })

    stats = _get_stats(estudiante)
    context = {
        'estudiante':    estudiante,
        'materias_data': materias_data,
        **stats,
    }
    return render(request, 'alumno/materias_alumno.html', context)


# ─────────────────────────────────────────
# TAREAS
# ─────────────────────────────────────────

@login_required
def tareas_alumno(request):
    estudiante = _get_estudiante(request)
    if not estudiante:
        return render(request, 'alumno/tareas_alumno.html', {
            'tareas': [], 'total_tareas': 0,
            'pendientes': 0, 'entregadas': 0, 'vencidas': 0,
        })

    # Tareas interactivas de la app tareas
    tareas_interactivas = Tareas.objects.all().order_by('fecha_entrega')

    # Tareas del docente para el curso del estudiante
    tareas_docente = Tarea.objects.filter(
        asignacion__curso=estudiante.curso
    ).select_related('asignacion__materia', 'periodo').order_by('-fecha_limite')

    context = {
        'estudiante':          estudiante,
        'tareas':              tareas_interactivas,
        'tareas_docente':      tareas_docente,
        'total_tareas':        tareas_docente.count(),
        'pendientes':          tareas_docente.filter(estado='pendiente').count(),
        'entregadas':          tareas_docente.filter(estado='entregada').count(),
        'vencidas':            tareas_docente.filter(estado='vencida').count(),
    }
    return render(request, 'alumno/tareas_alumno.html', context)


@login_required
def detalle_tarea(request, tarea_id):
    tarea = get_object_or_404(Tareas, id=tarea_id)

    resultados       = {}
    puntaje_total    = 0
    puntaje_obtenido = 0

    if request.method == 'POST':
        for pregunta in tarea.preguntas.all():
            respuesta_usuario = request.POST.get(f'pregunta_{pregunta.id}')
            if respuesta_usuario:
                correcta = RespuestaCorrecta.objects.get(pregunta=pregunta)
                es_correcta = (
                    respuesta_usuario.strip().lower()
                    == correcta.respuesta.strip().lower()
                )
                RespuestaEstudiante.objects.create(
                    pregunta=pregunta,
                    respuesta=respuesta_usuario,
                    es_correcta=es_correcta,
                )
                resultados[pregunta.id] = es_correcta
                puntaje_total += pregunta.puntaje
                if es_correcta:
                    puntaje_obtenido += pregunta.puntaje

    return render(request, 'tareas/alumno/detalle_tareas.html', {
        'tarea':            tarea,
        'resultados':       resultados,
        'puntaje_total':    puntaje_total,
        'puntaje_obtenido': puntaje_obtenido,
    })


# ─────────────────────────────────────────
# CALIFICACIONES (POR PERIODO Y MATERIA)
# ─────────────────────────────────────────

@login_required
def calificaciones_alumno(request):
    estudiante = _get_estudiante(request)
    if not estudiante:
        return render(request, 'alumno/calificaciones_alumno.html', {})

    periodos = PeriodoAcademico.objects.all().order_by('numero')

    # Periodo seleccionado (por defecto el activo)
    periodo_id  = request.GET.get('periodo')
    periodo_sel = None
    if periodo_id:
        periodo_sel = get_object_or_404(PeriodoAcademico, id=periodo_id)
    else:
        periodo_sel = PeriodoAcademico.objects.filter(activo=True).first()

    # Calificaciones del estudiante agrupadas por materia para el periodo
    asignaciones = AsignacionDocente.objects.filter(
        curso=estudiante.curso
    ).select_related('materia', 'docente')

    tabla = []
    promedios_periodo = []
    for asig in asignaciones:
        cal = Calificacion.objects.filter(
            estudiante=estudiante,
            asignacion=asig,
            periodo=periodo_sel,
        ).first()
        tabla.append({
            'materia':  asig.materia,
            'docente':  asig.docente,
            'cal':      cal,
            'promedio': cal.promedio if cal else None,
        })
        if cal:
            promedios_periodo.append(cal.promedio)

    promedio_periodo = round(
        sum(promedios_periodo) / len(promedios_periodo), 2
    ) if promedios_periodo else 0

    stats = _get_stats(estudiante)
    context = {
        'estudiante':       estudiante,
        'periodos':         periodos,
        'periodo_sel':      periodo_sel,
        'tabla':            tabla,
        'promedio_periodo': promedio_periodo,
        **stats,
    }
    return render(request, 'alumno/calificaciones_alumno.html', context)


# ─────────────────────────────────────────
# ASISTENCIA (POR MATERIA)
# ─────────────────────────────────────────

@login_required
def asistencia_alumno(request):
    estudiante = _get_estudiante(request)
    if not estudiante:
        return render(request, 'alumno/asistencia_alumno.html', {})

    # Asignaciones del curso para filtrar por materia
    asignaciones = AsignacionDocente.objects.filter(
        curso=estudiante.curso
    ).select_related('materia', 'docente')

    asignacion_id  = request.GET.get('asignacion')
    asignacion_sel = None

    if asignacion_id:
        asignacion_sel = get_object_or_404(
            AsignacionDocente, id=asignacion_id, curso=estudiante.curso
        )
        asistencias = Asistencia.objects.filter(
            estudiante=estudiante, asignacion=asignacion_sel
        ).order_by('-fecha')
    else:
        # Vista general — todas las asistencias
        asistencias = Asistencia.objects.filter(
            estudiante=estudiante
        ).select_related('asignacion__materia').order_by('-fecha')

    total    = asistencias.count()
    presentes = asistencias.filter(estado='presente').count()
    tardanzas = asistencias.filter(estado='tardanza').count()
    ausentes  = asistencias.filter(estado='ausente').count()
    porcentaje = round((presentes / total) * 100) if total > 0 else 0

    # Resumen por materia
    resumen_materias = []
    for asig in asignaciones:
        asis_materia = Asistencia.objects.filter(
            estudiante=estudiante, asignacion=asig
        )
        t = asis_materia.count()
        p = asis_materia.filter(estado='presente').count()
        resumen_materias.append({
            'asignacion': asig,
            'total':      t,
            'presentes':  p,
            'ausentes':   asis_materia.filter(estado='ausente').count(),
            'tardanzas':  asis_materia.filter(estado='tardanza').count(),
            'porcentaje': round((p / t) * 100) if t > 0 else 0,
        })

    stats = _get_stats(estudiante)
    context = {
        'estudiante':       estudiante,
        'asignaciones':     asignaciones,
        'asignacion_sel':   asignacion_sel,
        'asistencias':      asistencias,
        'resumen_materias': resumen_materias,
        'total':            total,
        'presentes':        presentes,
        'tardanzas':        tardanzas,
        'ausentes':         ausentes,
        'porcentaje':       porcentaje,
        **stats,
    }
    return render(request, 'alumno/asistencia_alumno.html', context)


# ─────────────────────────────────────────
# MENSAJES
# ─────────────────────────────────────────

@login_required
def mensajes_alumno(request):
    estudiante = _get_estudiante(request)
    if not estudiante:
        return render(request, 'alumno/mensajes_alumno.html', {})

    mensajes = Mensaje.objects.filter(
        estudiante=estudiante
    ).order_by('fecha')

    Mensaje.objects.filter(
        estudiante=estudiante, enviado_por='docente', leido=False
    ).update(leido=True)

    if request.method == 'POST':
        contenido = request.POST.get('contenido', '').strip()
        if contenido:
            # Busca el docente del primer mensaje o el primero disponible del curso
            docente = (
                Mensaje.objects.filter(estudiante=estudiante)
                .values_list('docente', flat=True)
                .first()
            )
            if not docente:
                asig = AsignacionDocente.objects.filter(
                    curso=estudiante.curso
                ).first()
                docente = asig.docente if asig else None

            if docente:
                if not isinstance(docente, Docente):
                    docente = Docente.objects.get(id=docente)
                Mensaje.objects.create(
                    docente=docente,
                    estudiante=estudiante,
                    contenido=contenido,
                    enviado_por='estudiante',
                )
        return redirect('mensajes_alumno')

    sin_leer = mensajes.filter(leido=False, enviado_por='docente').count()
    enviados = mensajes.filter(enviado_por='estudiante').count()

    context = {
        'estudiante': estudiante,
        'mensajes':   mensajes,
        'sin_leer':   sin_leer,
        'enviados':   enviados,
    }
    return render(request, 'alumno/mensajes_alumno.html', context)


# ─────────────────────────────────────────
# LOGROS
# ─────────────────────────────────────────

@login_required
def logros_alumno(request):
    estudiante = _get_estudiante(request)
    if not estudiante:
        return render(request, 'alumno/logros_alumno.html', {
            'promedio_general': 0,
            'porcentaje_asistencia': 0,
            'total_logros': 0,
            'logros_por_desbloquear': 5,
        })

    stats = _get_stats(estudiante)
    context = {
        'estudiante': estudiante,
        'logros_por_desbloquear': max(0, 5 - stats['total_logros']),
        **stats,
    }
    return render(request, 'alumno/logros_alumno.html', context)


# ─────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────

@login_required
def configuracion_alumno(request):
    estudiante = _get_estudiante(request)
    if not estudiante:
        return redirect('iniciar_sesion')

    if request.method == 'POST':
        estudiante.nombre = request.POST.get('nombre', estudiante.nombre).strip()
        estudiante.correo = request.POST.get('correo', estudiante.correo).strip()
        estudiante.save()
        return redirect('configuracion_alumno')

    return render(request, 'alumno/configuracion_alumno.html', {'estudiante': estudiante})
