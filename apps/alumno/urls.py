from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_alumno, name='dashboard_alumno'),
    path('materias/', views.materias_alumno, name='materias_alumno'),
    path('tareas/', views.tareas_alumno, name='tareas_alumno'),
    path('tareas/<int:tarea_id>/', views.detalle_tarea, name='detalle_tarea'),  # ← nueva
    path('calificaciones/', views.calificaciones_alumno, name='calificaciones_alumno'),
    path('asistencia/', views.asistencia_alumno, name='asistencia_alumno'),
    path('mensajes/', views.mensajes_alumno, name='mensajes_alumno'),
    path('logros/', views.logros_alumno, name='logros_alumno'),
    path('configuracion/', views.configuracion_alumno, name='configuracion_alumno'),
]