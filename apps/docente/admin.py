# apps/docente/admin.py
from django.contrib import admin
from .models import (
    Curso, Materia, Docente, AsignacionDocente,
    Estudiante, Calificacion, Tarea, Asistencia, Mensaje
)

@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'correo', 'usuario')
    search_fields = ('nombre', 'correo')

@admin.register(AsignacionDocente)
class AsignacionDocenteAdmin(admin.ModelAdmin):
    list_display  = ('docente', 'materia', 'curso')
    list_filter   = ('curso', 'materia', 'docente')

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'correo', 'curso', 'usuario')
    list_filter   = ('curso',)
    search_fields = ('nombre', 'correo')

@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'asignacion', 'tarea', 'parcial', 'examen', 'promedio')
    list_filter  = ('asignacion__curso', 'asignacion__materia', 'asignacion__docente')

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'asignacion', 'fecha_limite', 'estado')
    list_filter  = ('estado', 'asignacion__curso')

admin.site.register(Curso)
admin.site.register(Materia)
admin.site.register(Asistencia)
admin.site.register(Mensaje)