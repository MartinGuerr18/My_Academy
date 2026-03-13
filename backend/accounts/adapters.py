from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
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
            raise ValidationError(
                f'Solo se permiten correos @{DOMINIO_VALIDO}'
            )

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        email = user.email

        # Asignar rol automáticamente igual que en el registro manual
        user.rol = detectar_rol(email)
        user.matricula = None
        user.save()
        return user