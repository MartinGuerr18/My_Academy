from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('novedad/<int:pk>/', views.detalle_novedad, name='detalle_novedad'),
]