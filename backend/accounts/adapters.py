from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
import re

DOMINIO_VALIDO = 'itses.edu.mx'

def detectar_rol(email):
    local = email.split('@')[0]
    if re.search(r'\d', local):
        return 'alumno'
    return 'docente'

class GoogleAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get('email', '')

        # Rechazar correos que no sean institucionales
        if not email.endswith(f'@{DOMINIO_VALIDO}'):
            raise ImmediateHttpResponse(
                redirect(f'/login/?error=Solo+se+permiten+correos+%40{DOMINIO_VALIDO}')
            )

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        email = user.email
        user.rol = detectar_rol(email)
        user.username = email.split('@')[0]
        user.save()
        return user

    def is_open_for_signup(self, request, sociallogin):
        # Permite signup automático sin mostrar formulario
        return True