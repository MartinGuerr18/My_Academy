from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Columnas que se ven en la lista de usuarios
    list_display = ('username', 'email', 'matricula', 'rol', 'is_active')
    # Filtros en la barra lateral
    list_filter = ('rol', 'is_active')
    # Agrega nuestros campos extra al formulario de edición
    fieldsets = UserAdmin.fieldsets + (
        ('Datos My Academy', {'fields': ('matricula', 'rol')}),
    )