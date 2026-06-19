from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'


class User(AbstractUser):
    nombre = models.CharField('Nombre', max_length=100, blank=True)
    role   = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='usuarios'
    )
    # El curso del estudiante lo maneja apps.docente.Estudiante
    # No se duplica aquí para evitar dependencias circulares

    def __str__(self):
        return self.nombre if self.nombre else self.username

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'