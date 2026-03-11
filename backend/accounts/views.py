from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username_input = request.POST.get('username')
        password = request.POST.get('password')

        # Si el usuario escribió un email, buscamos el username real
        if '@' in username_input:
            try:
                user_obj = User.objects.get(email=username_input)
                username_input = user_obj.username
            except User.DoesNotExist:
                username_input = None

        user = authenticate(request, username=username_input, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)  # destruye la sesión
    return redirect('login')

from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def home_view(request):
    return render(request, 'accounts/home.html')

from .forms import RegistroForm

def registro_view(request):
    # Si ya está autenticado no necesita registrarse
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()  # guarda en PostgreSQL con contraseña encriptada
            messages.success(request, 'Cuenta creada exitosamente. Inicia sesión.')
            return redirect('login')
        # Si hay errores el form los carga automáticamente
    else:
        form = RegistroForm()  # GET → formulario vacío

    return render(request, 'accounts/registro.html', {'form': form})