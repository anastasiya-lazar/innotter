from coreapp.models import User
from django.utils.deprecation import MiddlewareMixin
from coreapp.services.auth_service import AuthService
import jwt
from django.contrib.auth.models import AnonymousUser
from coreapp.services.exceptions import UserNotFoundException


class SessionAuthCSRFDisableMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        setattr(request, "_dont_enforce_csrf_checks", True)
        response = self.get_response(request)
        return response


class JWTMiddleware(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        access_token = None
        authorization_header = request.META.get("HTTP_AUTHORIZATION")
        auth = AuthService()
        if authorization_header:
            try:
                token_type, token = authorization_header.split(" ")
                if token_type.lower() == "bearer":
                    access_token = token
            except ValueError:
                request.user = AnonymousUser()
        try:
            if access_token:
                user_id = auth.decode_token(access_token)
                user = User.objects.filter(pk=user_id).first()
                if not user:
                    raise UserNotFoundException
                request.user = user
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, jwt.DecodeError, IndexError):
            request.user = AnonymousUser()
