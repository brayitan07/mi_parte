from django.db import models

# Create your models here.


class Tareas(models.Model):
    titulo = models.CharField('Título', max_length=100)
    descripcion = models.TextField('Descripción')
    fecha_creacion = models.DateField('Fecha de creación', auto_now_add=True)
    fecha_entrega = models.DateField('Fecha de entrega', blank=True, null=True, default=None, )

    def __str__(self):
        return self.titulo


class RecursoTareas(models.Model):

    TIPOS = [
        ('video', 'Video'),
        ('pdf', 'PDF'),
        ('imagen', 'Imagen'),
        ('documento', 'Documento'),
        ('url', 'URL'),
    ]

    recurso_tarea = models.ForeignKey(
        Tareas,
        on_delete=models.CASCADE,
        related_name='recursos'
    )

    tipo = models.CharField(max_length=20, choices=TIPOS)

    archivo = models.FileField(
        upload_to='actividades/',
        blank=True,
        null=True
    )

    url = models.URLField(
        blank=True,
        null=True
    )


class Pregunta(models.Model):

    TIPOS = [
        ('abierta', 'Respuesta abierta'),
        ('opcion_multiple', 'Opción múltiple'),
    ]

    recurso_tarea = models.ForeignKey(
        Tareas,
        on_delete=models.CASCADE,
        related_name='preguntas'
    )

    enunciado = models.TextField()

    tipo = models.CharField(
        max_length=20,
        choices=TIPOS
    )

    orden = models.PositiveIntegerField(default=1)


class OpcionRespuesta(models.Model):

    pregunta = models.ForeignKey(
        Pregunta,
        on_delete=models.CASCADE,
        related_name='opciones'
    )

    texto = models.CharField(max_length=255)

    es_correcta = models.BooleanField(default=False)


class Respuesta(models.Model):

    """estudiante = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )"""

    pregunta = models.ForeignKey(
        Pregunta,
        on_delete=models.CASCADE
    )

    respuesta_texto = models.TextField(
        blank=True,
        null=True
    )

    opcion_seleccionada = models.ForeignKey(
        OpcionRespuesta,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    fecha = models.DateTimeField(auto_now_add=True)