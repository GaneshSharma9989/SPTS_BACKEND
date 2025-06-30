import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from django.http import JsonResponse

def generate_token(user):
    payload = {
        'id': user.id,
        'username': user.username,
        'exp': datetime.now(timezone.utc) + timedelta(days=1)
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

def jwt_required(view_func):
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({'error': 'Authorization header missing or invalid'}, status=401)

        token = auth_header.split(' ')[1]
        try:
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            request.user_id = decoded['id']
            return view_func(request, *args, **kwargs)
        except ExpiredSignatureError:
            return JsonResponse({'error': 'Token expired'}, status=401)
        except InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=401)

    return wrapper
