from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_docente, name='dashboard_docente'),
    path('cursos/', views.cursos_docente, name='cursos_docente'),
    path('tareas/', views.tarea_docente, name='tarea_docente'),
    path('tareas/eliminar/<int:id>/', views.eliminar_tarea, name='eliminar_tarea'),
    path('calificaciones/', views.calificaciones_docente, name='calificaciones_docente'),
    path('calificaciones/guardar/', views.guardar_todas_calificaciones, name='guardar_nota'),
    path('asistencia/', views.asistencia_docente, name='asistencia_docente'),
    path('mensajes/', views.mensajes_docente, name='mensajes_docente'),
    path('configuracion/', views.configuracion_docente, name='configuracion_docente'),
]