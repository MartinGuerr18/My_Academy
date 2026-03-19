from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', RedirectView.as_view(pattern_name='login'), name='index'),  # ← redirige a login
    path('', include('accounts.urls')),
    path('', include('novedades.urls')),
]