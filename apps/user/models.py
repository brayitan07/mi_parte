from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    nombre = models.CharField('Nombre', max_length=100)

    def __str__(self):
        return self.nombre if self.nombre else self.username