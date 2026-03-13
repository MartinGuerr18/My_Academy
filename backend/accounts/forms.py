from django import forms
from .models import User
import re

DOMINIO_VALIDO = 'itses.edu.mx'

def detectar_rol(email):
   
    local = email.split('@')[0]  # parte antes del @
    if re.search(r'\d', local):  # si tiene al menos un número
        return 'alumno'
    return 'docente'


class RegistroForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['email', 'matricula', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower().strip()

        # Validar dominio institucional
        if not email.endswith(f'@{DOMINIO_VALIDO}'):
            raise forms.ValidationError(
                f'Solo se permiten correos institucionales @{DOMINIO_VALIDO}'
            )

        # Validar que no exista ya ese email
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo ya está registrado')

        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data['email']

        # Username generado del email
        user.username = email.split('@')[0]

        # Rol detectado automáticamente del patrón del correo
        user.rol = detectar_rol(email)

        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user