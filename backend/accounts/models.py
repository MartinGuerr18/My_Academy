from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# ======================
# USUARIO (Custom User)
# ======================

class User(AbstractUser):

    ROL_CHOICES = [
        ('USUARIO', 'Usuario'),
        ('ADMIN', 'Administrador'),
        ('DOCENTE', 'Docente'),
    ]

    matricula = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True
    )

    rol = models.CharField(
        max_length=20,
        choices=ROL_CHOICES,
        default='USUARIO'
    )

    avatar = models.CharField(
        max_length=100,
        default='iniciales'
    )

    def __str__(self):
        return f"{self.username} ({self.rol})"


# ======================
# MATERIA
# ======================

class Materia(models.Model):

    nombre = models.CharField(max_length=150)

    cuatrimestre = models.IntegerField()

    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


# ======================
# PERIODO
# ======================

class Periodo(models.Model):

    PERIODOS = [
        ('Q1','Q1'),('Q2','Q2'),('Q3','Q3'),('Q4','Q4'),
        ('Q5','Q5'),('Q6','Q6'),('Q7','Q7'),
        ('Q8','Q8'),('Q9','Q9'),('Q10','Q10'),
        ('Q11','Q11'),('Q12','Q12'),('Q13','Q13'),('Q14','Q14')
    ]

    nombre = models.CharField(
        max_length=3,
        choices=PERIODOS
    )

    anio = models.IntegerField()

    numero = models.IntegerField()

    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.anio}"


# ======================
# CALIFICACION
# ======================

class Calificacion(models.Model):

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    materia = models.ForeignKey(
        Materia,
        on_delete=models.CASCADE
    )

    periodo = models.ForeignKey(
        Periodo,
        on_delete=models.SET_NULL,
        null=True
    )

    valor_numerico = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True
    )


# ======================
# NOVEDAD
# ======================

class Novedad(models.Model):

    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    titulo = models.CharField(max_length=200)

    contenido = models.TextField()

    fecha_publicacion = models.DateTimeField(
        auto_now_add=True
    )


# ======================
# OPINION
# ======================

class Opinion(models.Model):

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    materia = models.ForeignKey(
        Materia,
        on_delete=models.CASCADE
    )

    novedad = models.ForeignKey(
        Novedad,
        on_delete=models.SET_NULL,
        null=True
    )

    comentario = models.TextField()

    estrellas = models.IntegerField()

    fecha_hora = models.DateTimeField(
        auto_now_add=True
    )


# ======================
# REUNION
# ======================

class Reunion(models.Model):

    PLATAFORMAS = [
        ('Zoom', 'Zoom'),
        ('Meet', 'Meet'),
    ]

    materia = models.ForeignKey(
        Materia,
        on_delete=models.CASCADE
    )

    titulo = models.CharField(max_length=200)

    fecha_hora = models.DateTimeField()

    plataforma = models.CharField(
        max_length=10,
        choices=PLATAFORMAS
    )

    link = models.URLField(
        null=True,
        blank=True
    )