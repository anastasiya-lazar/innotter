import os
import jwt
from datetime import datetime, timedelta
from coreapp.models import User
from coreapp.services.exceptions import RefreshTokenException


class AuthService:
    key = os.environ.get('JWT_SECRET')
    JWT_ACCESS_TTL = int(os.environ.get('JWT_ACCESS_TTL'))
    JWT_REFRESH_TTL = int(os.environ.get('JWT_REFRESH_TTL'))
    JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM')

    def create_access_token(self, user_id):
        payload = {
            'iss': 'backend-api',
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(minutes=self.JWT_ACCESS_TTL),
            'type': 'access'
        }
        access = jwt.encode(payload, self.key, algorithm=self.JWT_ALGORITHM)
        return access

    def create_refresh_token(self, user_id):
        payload = {
            'iss': 'backend-api',
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(weeks=self.JWT_REFRESH_TTL),
            'type': 'access'
        }
        refresh = jwt.encode(payload, self.key, algorithm=self.JWT_ALGORITHM)
        return refresh

    def decode_token(self, token):
        payload = jwt.decode(token, self.key, algorithms=self.JWT_ALGORITHM)
        user_id = payload['user_id']
        return user_id

    def generate_access_and_refresh_token(self, user_id):
        access_token = self.create_access_token(user_id)
        refresh_token = self.create_refresh_token(user_id)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def get_user_and_generate_tokens(self, *args):
        email = args[0]
        user = User.objects.get(email=email)
        tokens = self.generate_access_and_refresh_token(user.id)
        return tokens

    def validate_token(self, token):
        try:
            jwt.decode(token, self.key, algorithms=self.JWT_ALGORITHM)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, jwt.DecodeError):
            raise RefreshTokenException

