import os
from coreapp.models import User
from django.utils.deprecation import MiddlewareMixin
from coreapp.authentication import validate_token
from rest_framework.exceptions import APIException



key = os.environ.get('JWT_SECRET')  

class JWTMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.path.startswith('/login/'):
          return None
        jwt_token = request.headers.get('authorization', None)
        if jwt_token:
                user_id = validate_token(jwt_token)
                user = User.objects.get(pk=user_id)
                if user:
                    request.user = user   
        else:
            raise APIException("Authorization not found, Please send valid token in headers")
            

class SessionAuthCSRFDisableMiddleware:
    def __init__ (self, get_response):
          self.get_response = get_response

    def __call__(self, request):
         setattr(request, '_dont_enforce_csrf_checks', True)
         response = self.get_response(request)
         return response