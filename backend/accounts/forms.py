import re
from django import forms
from .models import User

DOMINIO_VALIDO = 'itses.edu.mx'

def detectar_rol(email):
    local = email.split('@')[0]
    if re.search(r'\d', local):
        return 'alumno'
    return 'docente'

class RegistroForm(forms.ModelForm):
    first_name = forms.CharField(
        label='Nombre',
        max_length=50,
    )
    last_name = forms.CharField(
        label='Apellido',
        max_length=50,
    )
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'matricula', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower().strip()
        if not email.endswith(f'@{DOMINIO_VALIDO}'):
            raise forms.ValidationError(
                f'Solo se permiten correos institucionales @{DOMINIO_VALIDO}'
            )
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo ya está registrado')
        return email

    def clean_matricula(self):
        matricula = self.cleaned_data.get('matricula', '').strip()
        # Validar que sea solo dígitos y entre 6 y 10 caracteres
        if not matricula.isdigit():
            raise forms.ValidationError('La matrícula solo debe contener números')
        if not (6 <= len(matricula) <= 10):
            raise forms.ValidationError('La matrícula debe tener entre 6 y 10 dígitos')
        if User.objects.filter(matricula=matricula).exists():
            raise forms.ValidationError('Esta matrícula ya está registrada')
        return matricula

    def clean_password1(self):
        password = self.cleaned_data.get('password1', '')
        # Mínimo 8 caracteres
        if len(password) < 8:
            raise forms.ValidationError('La contraseña debe tener mínimo 8 caracteres')
        # Al menos 1 mayúscula
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError('La contraseña debe tener al menos 1 mayúscula')
        # Al menos 1 número
        if not re.search(r'\d', password):
            raise forms.ValidationError('La contraseña debe tener al menos 1 número')
        return password

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
        user.username = email.split('@')[0]
        user.rol = detectar_rol(email)
        user.first_name = self.cleaned_data['first_name']   # ← nuevo
        user.last_name = self.cleaned_data['last_name']     # ← nuevo
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user