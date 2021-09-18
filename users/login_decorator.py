import jwt

from django.http import JsonResponse

from my_settings import SECRET_KEY, ALGORITHM
from users.models import User


def token_validation_decorator(func):
    def wrapper(self, request):
        try:
            access_token = request.headers.get('Authorization')
            if not access_token:
                return JsonResponse({'message': 'KEY_ERROR'}, status=400)

            payload = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)
            user = User.objects.get(id=payload['user_id'])
            request.user = user
            return func(self, request)

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        except jwt.exceptions.ExpiredSignatureError:
            return JsonResponse({'message': 'TOKEN_EXPIRED'}, status=403)
    return wrapper