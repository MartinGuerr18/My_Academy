from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Novedad

@login_required(login_url='login')
def home_view(request):
    # Últimas 3 novedades activas ordenadas por fecha descendente
    novedades = Novedad.objects.filter(activa=True).order_by('-fecha_publicacion')[:3]
    return render(request, 'novedades/home.html', {'novedades': novedades})

@login_required(login_url='login')
def detalle_novedad(request, pk):
    # Busca la novedad por ID o devuelve 404 — equivalente a un GET /novedades/:id
    novedad = get_object_or_404(Novedad, pk=pk, activa=True)
    return render(request, 'novedades/detalle.html', {'novedad': novedad})