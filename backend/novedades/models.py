from django.db import models
from accounts.models import User

class Novedad(models.Model):
    CATEGORIA_CHOICES = [
        ('evaluacion', '📊 Evaluaciones'),
        ('inscripcion', '🖊 Inscripciones'),
        ('taller', '🖊 Talleres'),
        ('general', '📢 General'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='general')
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ['-fecha_publicacion']  # más recientes primero

    def __str__(self):
        return self.titulo