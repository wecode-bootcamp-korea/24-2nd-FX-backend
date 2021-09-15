import json
import re
import bcrypt

from django.views import View
from django.http import JsonResponse
from django.db.utils import DataError

from users.models import User


class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        email_format       = re.compile('\w+[@]\w+[.]\w+')
        password_format    = re.compile('^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,20}$')

        try:
            if not email_format.search(data['email']):
                return JsonResponse({'message': 'INVALID_EMAIL_FORMAT'}, status=400)
            if not password_format.match(data['password']):
                return JsonResponse({'message': 'INVALID_PASSWORD_FORMAT'})

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message': 'USER_ALREADY_EXISTS'}, status=400)

            salt = bcrypt.gensalt()
            encoded_passwrod = data['password'].encode('utf-8')
            hashed_password  = bcrypt.hashpw(encoded_passwrod, salt)
            decoded_password = hashed_password.decode('utf-8')

            User.objects.create(
                name        = data['name'],
                email       = data['email'],
                password    = decoded_password,
                signup_type = data['signup_type']
            )
            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEYERROR'}, status=400)
        except DataError:
            return JsonResponse({'message': 'DATA_TOO_LONG'})
