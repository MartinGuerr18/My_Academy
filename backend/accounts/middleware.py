from django.contrib.auth import get_user_model
from .jwt_utils import verificar_token

User = get_user_model()

class JWTAuthMiddleware:
    """
    Middleware que lee el JWT de la cookie en cada petición
    y autentica al usuario automáticamente.
    Equivalente al AuthGuard de Angular.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.COOKIES.get('access_token')

        if token:
            payload = verificar_token(token)
            if payload:
                try:
                    user = User.objects.get(id=payload['user_id'])
                    request.user = user
                except User.DoesNotExist:
                    pass

        response = self.get_response(request)
        return response