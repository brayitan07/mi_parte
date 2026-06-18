from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_docente, name='dashboard_docente'),
    path('cursos/', views.cursos_docente, name='cursos_docente'),
    path('tareas/', views.tarea_docente, name='tarea_docente'),
    path('tareas/eliminar/<int:id>/', views.eliminar_tarea, name='eliminar_tarea'),
    path('calificaciones/', views.calificaciones_docente, name='calificaciones_docente'),
    path('calificaciones/guardar/', views.guardar_nota, name='guardar_nota'),
    path('calificaciones/reporte/', views.reporte_notas, name='reporte_notas'),
    path('calificaciones/reporte/pdf/', views.exportar_reporte_pdf, name='exportar_reporte_pdf'),
    path('calificaciones/reporte/excel/', views.exportar_reporte_excel, name='exportar_reporte_excel'),
    path('asistencia/', views.asistencia_docente, name='asistencia_docente'),
    path('asistencia/guardar/', views.guardar_asistencia, name='guardar_asistencia'),  # ← nueva
    path('mensajes/', views.mensajes_docente, name='mensajes_docente'),
    path('configuracion/', views.configuracion_docente, name='configuracion_docente'),
    path('asistencia/historial/', views.historial_asistencia, name='historial_asistencia'),
    path('asistencia/eliminar/', views.eliminar_asistencia, name='eliminar_asistencia'),
    path('calificaciones/eliminar-nota/', views.eliminar_nota, name='eliminar_nota'),
]