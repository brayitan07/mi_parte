from django.db import models
from embed_video.fields import EmbedVideoField


class Tareas(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    video = EmbedVideoField(blank=True, null=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_entrega = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.titulo)


class Imagen(models.Model):
    tarea = models.ForeignKey(Tareas, on_delete=models.CASCADE, related_name="imagenes")
    imagen = models.ImageField(null=True, blank=True, upload_to="imagenes/")

    def __str__(self):
        return str(self.imagen)


class Pregunta(models.Model):
    TIPOS = (
        ("texto", "Respuesta abierta"),
        ("opcion", "Opción múltiple"),
    )

    tarea = models.ForeignKey(
        Tareas, on_delete=models.CASCADE, related_name="preguntas"
    )

    enunciado = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPOS)

    puntaje = models.IntegerField(default=1)  # 👈 NUEVO

    def __str__(self):
        return self.enunciado


class Opcion(models.Model):
    pregunta = models.ForeignKey(
        Pregunta, on_delete=models.CASCADE, related_name="opciones"
    )

    texto = models.CharField(max_length=255)
    es_correcta = models.BooleanField(default=False)

    def __str__(self):
        return self.texto


class RespuestaCorrecta(models.Model):
    pregunta = models.OneToOneField(Pregunta, on_delete=models.CASCADE)

    respuesta = models.CharField(max_length=255)

    def __str__(self):
        return self.respuesta


class RespuestaEstudiante(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)

    respuesta = models.TextField()

    es_correcta = models.BooleanField(default=False)

    fecha = models.DateTimeField(auto_now_add=True)



