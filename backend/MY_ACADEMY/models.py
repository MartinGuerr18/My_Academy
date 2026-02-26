from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    # Definimos los roles según tus requerimientos
    ROLE_CHOICES = (
        ('alumno', 'Alumno'),
        ('docente', 'Docente'),
        ('admin', 'Administrador'),
    )
    rol = models.CharField(max_length=10, choices=ROLE_CHOICES, default='alumno')
    matricula = models.CharField(max_length=20, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.username} - {self.rol}"
