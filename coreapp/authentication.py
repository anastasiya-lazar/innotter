import os
import jwt
from datetime import datetime, timedelta

key = os.environ.get('JWT_SECRET')
JWT_ACCESS_TTL = int(os.environ.get('JWT_ACCESS_TTL'))
JWT_REFRESH_TTL = int(os.environ.get('JWT_REFRESH_TTL'))
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM')


def create_access_token(user_id):
    payload = {
        'iss': 'backend-api',
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TTL),
        'type': 'access'
    }
    access = jwt.encode(payload, key, algorithm=JWT_ALGORITHM)
    return access


def create_refresh_token(user_id):
    payload = {
        'iss': 'backend-api',
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(weeks=JWT_REFRESH_TTL),
        'type': 'access'
    }
    refresh = jwt.encode(payload, key, algorithm=JWT_ALGORITHM)
    return refresh


def decode_token(token):
    payload = jwt.decode(token, key, algorithms=JWT_ALGORITHM)
    user_id = payload['user_id']
    return user_id
