from django.urls import path
from . import views

urlpatterns = [
    # Esto responderá a: /tareas/
    path('tareas', views.listar_tareas, name='listar_tareas'),
    # Esto responderá a: /tareas/crear/
    path('crear/', views.crear_tarea, name='crear_tarea'),
    path('editar/<int:tarea_id>/', views.editar_tarea, name='editar_tarea'),
    path('eliminar/<int:tarea_id>/', views.eliminar_tarea, name='eliminar_tarea'),
    path('detalle/<int:tarea_id>/', views.detalle_tarea, name='detalle_tarea'),
    path('reproductor/', views.reproductor, name='reproductor'),
    path('subir-imagen/', views.subir_imagen, name='subir_imagen'),
    path('responder/<int:tarea_id>/', views.responder_tarea, name='responder_tarea'),

]