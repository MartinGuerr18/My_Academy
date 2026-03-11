from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Roles disponibles en el sistema
    ROL_CHOICES = [
        ('alumno', 'Alumno'),
        ('docente', 'Docente'),
        ('admin', 'Administrador'),
    ]

    # Campos extra que necesita My Academy
    matricula = models.CharField(max_length=20, unique=True, null=True, blank=True)
    rol = models.CharField(max_length=10, choices=ROL_CHOICES, default='alumno')

    def __str__(self):
        # Lo que se muestra cuando imprimes un User
        # Equivalente a toString() en TypeScript
        return f"{self.username} ({self.rol})"