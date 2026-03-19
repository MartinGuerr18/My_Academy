from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User
from .jwt_utils import generar_token
from .forms import RegistroForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username_input = request.POST.get('username')
        password = request.POST.get('password')

        if '@' in username_input:
            try:
                user_obj = User.objects.get(email=username_input)
                username_input = user_obj.username
            except User.DoesNotExist:
                username_input = None

        user = authenticate(request, username=username_input, password=password)

        if user is not None:
            login(request, user)

            # Generar JWT y guardarlo en cookie HttpOnly
            token = generar_token(user)
            response = redirect('home')
            response.set_cookie(
                'access_token',
                token,
                max_age=86400,      # 24 horas en segundos
                httponly=True,      # No accesible desde JavaScript
                samesite='Lax',
            )
            return response
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    response = redirect('login')
    # Eliminar el JWT al cerrar sesión
    response.delete_cookie('access_token')
    return response

def registro_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada exitosamente. Inicia sesión.')
            return redirect('login')
    else:
        form = RegistroForm()

    return render(request, 'accounts/registro.html', {'form': form})