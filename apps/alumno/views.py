from django.shortcuts import render, redirect, get_object_or_404
from apps.tareas.models import Tareas, RespuestaCorrecta, RespuestaEstudiante
from apps.docente.models import Estudiante, Calificacion, Asistencia, Mensaje, Tarea, Docente
from django.utils import timezone

ESTUDIANTE_ID = 1

def get_estudiante():
    return Estudiante.objects.filter(id=ESTUDIANTE_ID).first()

def get_stats(estudiante):
    calificaciones = Calificacion.objects.filter(estudiante=estudiante)
    promedio_general = round(sum(c.promedio for c in calificaciones) / calificaciones.count(), 1) if calificaciones.exists() else 0
    asistencias = Asistencia.objects.filter(estudiante=estudiante)
    total_asis = asistencias.count()
    presentes = asistencias.filter(estado='presente').count()
    tardanzas = asistencias.filter(estado='tardanza').count()
    ausentes = asistencias.filter(estado='ausente').count()
    porcentaje_asistencia = round((presentes / total_asis) * 100) if total_asis > 0 else 0
    aprobadas = sum(1 for c in calificaciones if c.promedio >= 3.0)
    en_riesgo = sum(1 for c in calificaciones if c.promedio < 3.0)
    total_logros = sum([porcentaje_asistencia >= 90, promedio_general >= 4.5, promedio_general >= 3.0])
    return {
        'calificaciones': calificaciones,
        'promedio_general': promedio_general,
        'porcentaje_asistencia': porcentaje_asistencia,
        'presentes': presentes,
        'tardanzas': tardanzas,
        'ausentes': ausentes,
        'aprobadas': aprobadas,
        'en_riesgo': en_riesgo,
        'total_logros': total_logros,
    }

def dashboard_alumno(request):
    estudiante = get_estudiante()
    if not estudiante:
        return render(request, 'alumno/dashboard_alumno.html', {})
    stats = get_stats(estudiante)
    tareas = Tarea.objects.filter(curso=estudiante.curso)
    mensajes = Mensaje.objects.filter(estudiante=estudiante).order_by('-fecha')
    sin_leer = mensajes.filter(leido=False, enviado_por='docente').count()
    context = {
        'estudiante': estudiante,
        'tareas_pendientes': tareas.filter(estado='pendiente').count(),
        'mensajes_recientes': mensajes[:3],
        'mensajes_sin_leer': sin_leer,
        **stats,
    }
    return render(request, 'alumno/dashboard_alumno.html', context)

def materias_alumno(request):
    estudiante = get_estudiante()
    if not estudiante:
        return render(request, 'alumno/materias_alumno.html', {})
    stats = get_stats(estudiante)
    return render(request, 'alumno/materias_alumno.html', {'estudiante': estudiante, **stats})

def tareas_alumno(request):
    estudiante = get_estudiante()
    if not estudiante:
        return render(request, 'alumno/tareas_alumno.html', {})

    tareas_cal     = Tarea.objects.filter(curso=estudiante.curso).order_by('fecha_limite')
    tareas_detalle = Tareas.objects.all()

    context = {
        'estudiante':    estudiante,
        'tareas':        tareas_cal,
        'tareas_detalle': tareas_detalle,
        'total_tareas':  tareas_cal.count(),
        'pendientes':    tareas_cal.filter(estado='pendiente').count(),
        'entregadas':    tareas_cal.filter(estado='entregada').count(),
        'vencidas':      tareas_cal.filter(estado='vencida').count(),
    }
    return render(request, 'alumno/tareas_alumno.html', context)

def detalle_tarea(request, tarea_id):
    tarea = get_object_or_404(Tareas, id=tarea_id)

    resultados      = {}
    puntaje_total   = 0
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

def calificaciones_alumno(request):
    estudiante = get_estudiante()
    if not estudiante:
        return render(request, 'alumno/calificaciones_alumno.html', {})
    stats = get_stats(estudiante)
    return render(request, 'alumno/calificaciones_alumno.html', {'estudiante': estudiante, **stats})

def asistencia_alumno(request):
    estudiante = get_estudiante()
    if not estudiante:
        return render(request, 'alumno/asistencia_alumno.html', {})
    asistencias = Asistencia.objects.filter(estudiante=estudiante).order_by('-fecha')
    stats = get_stats(estudiante)
    return render(request, 'alumno/asistencia_alumno.html', {
        'estudiante': estudiante,
        'asistencias': asistencias,
        **stats,
    })

def mensajes_alumno(request):
    estudiante = get_estudiante()
    if not estudiante:
        return render(request, 'alumno/mensajes_alumno.html', {})
    mensajes = Mensaje.objects.filter(estudiante=estudiante).order_by('fecha')
    Mensaje.objects.filter(estudiante=estudiante, enviado_por='docente', leido=False).update(leido=True)
    if request.method == 'POST':
        contenido = request.POST.get('contenido')
        if contenido:
            docente = Docente.objects.filter(id=1).first()
            if docente:
                Mensaje.objects.create(
                    docente=docente, estudiante=estudiante,
                    contenido=contenido, enviado_por='estudiante'
                )
        return redirect('mensajes_alumno')
    sin_leer = mensajes.filter(leido=False, enviado_por='docente').count()
    enviados = mensajes.filter(enviado_por='estudiante').count()
    return render(request, 'alumno/mensajes_alumno.html', {
        'estudiante': estudiante,
        'mensajes':   mensajes,
        'sin_leer':   sin_leer,
        'enviados':   enviados,
    })

def logros_alumno(request):
    estudiante = get_estudiante()
    if not estudiante:
        return render(request, 'alumno/logros_alumno.html', {
            'promedio': 0,
            'porcentaje_asistencia': 0,
            'total_logros': 0,
            'logros_por_desbloquear': 5,
        })
    stats = get_stats(estudiante)
    return render(request, 'alumno/logros_alumno.html', {'estudiante': estudiante, **stats})

def configuracion_alumno(request):
    estudiante = get_estudiante()
    return render(request, 'alumno/configuracion_alumno.html', {'estudiante': estudiante})