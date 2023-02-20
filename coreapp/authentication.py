import os
import jwt
from datetime import datetime, timedelta
from rest_framework.exceptions import AuthenticationFailed


key = os.environ.get('JWT_SECRET') 
JWT_ACCESS_TTL = int(os.environ.get('JWT_ACCESS_TTL')) 
JWT_REFRESH_TTL = int(os.environ.get('JWT_REFRESH_TTL')) 


def create_access_token(id):
    payload = {
            'iss': 'backend-api',
            'user_id': id,
            'exp': datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TTL),
            'type': 'access'
        }
    access = jwt.encode(payload, key, algorithm='HS256')
    return access 


def create_refresh_token(id):
    payload = {
            'iss': 'backend-api',
            'user_id': id,
            'exp': datetime.utcnow() + timedelta(weeks=JWT_REFRESH_TTL),
            'type': 'access'
        }
    refresh = jwt.encode(payload, key, algorithm='HS256')
    return refresh


def validate_token(token):
    try:
       payload= jwt.decode(token, key, algorithms="HS256")
       user_id = payload['user_id']
       return user_id
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed( "Authentication token has expired")
    except (jwt.DecodeError, jwt.InvalidTokenError):
        raise AuthenticationFailed("Authorization has failed, Please send valid token.")
