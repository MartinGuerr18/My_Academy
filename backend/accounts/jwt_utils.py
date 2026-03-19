import jwt
from datetime import datetime, timedelta
from django.conf import settings

def generar_token(user):
    """
    Genera un JWT con expiración de 24 horas.
    Equivalente a JwtService.sign() en NestJS/Angular.
    """
    payload = {
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'rol': user.rol,
        'exp': datetime.utcnow() + timedelta(hours=24),
        'iat': datetime.utcnow(),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

def verificar_token(token):
    """
    Verifica y decodifica el JWT.
    Regresa el payload o None si es inválido/expirado.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None