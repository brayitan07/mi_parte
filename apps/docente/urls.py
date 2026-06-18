# apps/docente/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard_docente, name='dashboard_docente'),

    # Cursos
    path('cursos/', views.cursos_docente, name='cursos_docente'),

    # Tareas
    path('tareas/',                        views.tarea_docente,  name='tarea_docente'),
    path('tareas/crear/',                  views.crear_tarea,    name='crear_tarea'),
    path('tareas/<int:id>/',               views.detalle_tarea,  name='detalle_tarea'),
    path('tareas/<int:id>/editar/',        views.editar_tarea,   name='editar_tarea'),
    path('tareas/eliminar/<int:id>/',      views.eliminar_tarea, name='eliminar_tarea'),

    # Calificaciones
    path('calificaciones/',                views.calificaciones_docente, name='calificaciones_docente'),
    path('calificaciones/guardar/',        views.guardar_nota,           name='guardar_nota'),
    path('calificaciones/eliminar-nota/',  views.eliminar_nota,          name='eliminar_nota'),
    path('calificaciones/reporte/',        views.reporte_notas,          name='reporte_notas'),
    path('calificaciones/reporte/pdf/',    views.exportar_reporte_pdf,   name='exportar_reporte_pdf'),
    path('calificaciones/reporte/excel/',  views.exportar_reporte_excel, name='exportar_reporte_excel'),

    # Asistencia
    path('asistencia/',           views.asistencia_docente,  name='asistencia_docente'),
    path('asistencia/guardar/',   views.guardar_asistencia,  name='guardar_asistencia'),
    path('asistencia/historial/', views.historial_asistencia, name='historial_asistencia'),
    path('asistencia/eliminar/',  views.eliminar_asistencia, name='eliminar_asistencia'),

    # Mensajes
    path('mensajes/', views.mensajes_docente, name='mensajes_docente'),

    # Configuración
    path('configuracion/', views.configuracion_docente, name='configuracion_docente'),
]