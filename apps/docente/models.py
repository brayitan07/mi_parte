# apps/docente/models.py
from django.db import models
from django.conf import settings


class Curso(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'


class Materia(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Materia'
        verbose_name_plural = 'Materias'


class Docente(models.Model):
    usuario  = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='docente',
        null=True, blank=True
    )
    nombre   = models.CharField(max_length=100)
    correo   = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Docente'
        verbose_name_plural = 'Docentes'


class AsignacionDocente(models.Model):
    """Un docente puede dictar varias materias en varios cursos."""
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE, related_name='asignaciones')
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='asignaciones')
    curso   = models.ForeignKey(Curso,   on_delete=models.CASCADE, related_name='asignaciones')

    def __str__(self):
        return f"{self.docente} — {self.materia} — {self.curso}"

    class Meta:
        verbose_name = 'Asignación Docente'
        verbose_name_plural = 'Asignaciones Docentes'
        unique_together = ('docente', 'materia', 'curso')


class Estudiante(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='estudiante',
        null=True, blank=True
    )
    nombre  = models.CharField(max_length=100)
    correo  = models.EmailField(unique=True)
    curso   = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='estudiantes')

    def __str__(self):
        return f"{self.nombre} - {self.curso}"

    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'


class Calificacion(models.Model):
    estudiante = models.ForeignKey(Estudiante,        on_delete=models.CASCADE, related_name='calificaciones')
    asignacion = models.ForeignKey(AsignacionDocente, on_delete=models.CASCADE, related_name='calificaciones')
    tarea      = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    parcial    = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    examen     = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    fecha      = models.DateField(auto_now_add=True)

    @property
    def promedio(self):
        return round((self.tarea + self.parcial + self.examen) / 3, 2)

    @property
    def materia(self):
        return self.asignacion.materia

    @property
    def docente(self):
        return self.asignacion.docente

    def __str__(self):
        return f"{self.estudiante} — {self.asignacion.materia}: {self.promedio}"

    class Meta:
        verbose_name = 'Calificación'
        verbose_name_plural = 'Calificaciones'
        unique_together = ('estudiante', 'asignacion')


class Tarea(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('entregada', 'Entregada'),
        ('vencida',   'Vencida'),
    ]
    titulo            = models.CharField(max_length=200)
    descripcion       = models.TextField(blank=True)
    asignacion        = models.ForeignKey(AsignacionDocente, on_delete=models.CASCADE, related_name='tareas')
    fecha_limite      = models.DateField()
    estado            = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    entregas          = models.IntegerField(default=0)
    total_estudiantes = models.IntegerField(default=0)

    @property
    def materia(self):
        return self.asignacion.materia

    @property
    def curso(self):
        return self.asignacion.curso

    @property
    def docente(self):
        return self.asignacion.docente

    def __str__(self):
        return f"{self.titulo} — {self.asignacion.curso}"

    class Meta:
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'


class Asistencia(models.Model):
    ESTADO_CHOICES = [
        ('presente', 'Presente'),
        ('ausente',  'Ausente'),
        ('tardanza', 'Tardanza'),
    ]
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='asistencias')
    fecha      = models.DateField()
    estado     = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='presente')

    def __str__(self):
        return f"{self.estudiante} — {self.fecha}: {self.estado}"

    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        unique_together = ('estudiante', 'fecha')


class Mensaje(models.Model):
    docente     = models.ForeignKey(Docente,    on_delete=models.CASCADE, related_name='mensajes_enviados')
    estudiante  = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='mensajes')
    contenido   = models.TextField()
    enviado_por = models.CharField(max_length=10, choices=[('docente', 'Docente'), ('estudiante', 'Estudiante')])
    fecha       = models.DateTimeField(auto_now_add=True)
    leido       = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.enviado_por}: {self.contenido[:40]}"

    class Meta:
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'
        ordering = ['fecha']