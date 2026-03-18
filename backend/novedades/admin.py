from django.contrib import admin
from .models import Novedad

@admin.register(Novedad)
class NovedadAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'autor', 'fecha_publicacion', 'activa')
    list_filter = ('categoria', 'activa')
    search_fields = ('titulo', 'descripcion')