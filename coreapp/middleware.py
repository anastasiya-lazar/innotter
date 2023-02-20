import os
from coreapp.models import User
from django.utils.deprecation import MiddlewareMixin
from coreapp.authentication import decode_token
import jwt
from django.http import JsonResponse


class SessionAuthCSRFDisableMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
        response = self.get_response(request)
        return response


class JWTMiddleware(MiddlewareMixin):
    def process_request(self, request):

        if request.path.startswith(('/auth/login/', '/auth/refresh/', '/swagger/', '/admin/', '/redoc/')):
            return None

        access_token = None
        refresh_token = request.COOKIES.get('refresh_token', None)
        if not refresh_token:
            authorization_header = request.META.get('HTTP_AUTHORIZATION')
            if not authorization_header:
                return JsonResponse({'error': 'Authorization header is missing'}, status=401)
            try:
                token_type, token = authorization_header.split(' ')
                if token_type.lower() == 'bearer':
                    access_token = token
                elif token_type.lower() == 'refresh':
                    refresh_token = token
            except ValueError:
                return JsonResponse({'error': 'Malformed Authorization header'}, status=401)

            if not access_token and not refresh_token:
                return JsonResponse({'error': 'Invalid token type'}, status=401)

        try:
            if access_token:
                user_id = decode_token(access_token)
                user = User.objects.get(pk=user_id)
                if user:
                    request.user = user
            elif refresh_token:
                user_id = decode_token(refresh_token)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token has expired'}, status=401)
        except (jwt.InvalidTokenError, IndexError):
            return JsonResponse({'error': 'Token is invalid'}, status=401)

        response = self.get_response(request)
        return response