from coreapp.models import User
from django.utils.deprecation import MiddlewareMixin
from coreapp.authentication import decode_token
import jwt
from django.contrib.auth.models import AnonymousUser
 

class SessionAuthCSRFDisableMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
        response = self.get_response(request)
        return response


class JWTMiddleware(MiddlewareMixin):
    def process_request(self, request):
        access_token = None 
        refresh_token = request.COOKIES.get('refresh_token') 
        
        authorization_header =request.META.get('HTTP_AUTHORIZATION')
        if authorization_header:
            try:
                token_type, token = authorization_header.split(' ')
                if token_type.lower() == 'bearer':
                        access_token = token 
            except ValueError:
                request.user = AnonymousUser()
        try:
            if access_token:
                user_id = decode_token(access_token)
                user = User.objects.get(pk=user_id)
                if user:
                    request.user = user
            elif refresh_token:
                user_id = decode_token(refresh_token)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, jwt.DecodeError, IndexError):
            request.user = AnonymousUser()

