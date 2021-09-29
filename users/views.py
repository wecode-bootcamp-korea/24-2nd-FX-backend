import re
import jwt
import json
import bcrypt
import requests
from datetime import datetime, timedelta

from django.views import View
from django.http import JsonResponse
from django.shortcuts import redirect
from django.db.utils import DataError

from users.models import User
from users.kakao_api import KakaoApi
from my_settings import KAKAO_KEY, SECRET_KEY, ALGORITHM
from users.login_decorator import token_validation_decorator


class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        email_format       = re.compile('\w+[@]\w+[.]\w+')
        password_format    = re.compile('^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,20}$')

        try:
            if not email_format.search(data['email']):
                return JsonResponse({'message': 'INVALID_EMAIL_FORMAT'}, status=400)
            if not password_format.match(data['password']):
                return JsonResponse({'message': 'INVALID_PASSWORD_FORMAT'}, status=400)

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
                signup_type = User.SignupType.FLIX
            )
            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except DataError:
            return JsonResponse({'message': 'DATA_TOO_LONG'}, status=400)


class SignInView(View):
    def post(self, request):
        ENCODE_FORMAT = 'utf-8'
        algorithm     = ALGORITHM
        data          = json.loads(request.body)

        try:
            if data['signup_type'] != User.SignupType.FLIX.name:
                return JsonResponse({'message': 'LOGIN_TYPE_IS_NOT_FLIX'}, status=400)
            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message': 'USER_DOES_NOT_EXIST'}, status=400)

            user = User.objects.get(email=data['email'])
            if not bcrypt.checkpw(data['password'].encode(ENCODE_FORMAT), user.password.encode(ENCODE_FORMAT)):
                return JsonResponse({'message': 'INVALID_PASSWORD'}, status=403)

            access_token = jwt.encode({
                'user_id': user.id,
                'exp'    : datetime.utcnow() + timedelta(minutes=240)
                }, SECRET_KEY, algorithm=algorithm)
            return JsonResponse({
                'message': 'LOGIN_SUCCESS',
                'token': access_token
                }, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)


class GoogleLogInView(View):
    def post(self, request):

        try:
            user = request.headers.get('Authorization')
            data = json.loads(request.body)

            if not user:
                return JsonResponse({'message': 'INVALID_USER'}, status=401)

            User.objects.update_or_create(
                kakao_id    = data['google_id'],
                signup_type = 'GOOGLE',
                password    = '',
                defaults    = {'name': data['name']}
            )

            user_info = User.objects.get(kakao_id=data['google_id'])

            flix_access_token = jwt.encode({
                'user_id'    : user_info.id,
                'login_type' : 'GOOGLE',
                'exp'        : datetime.utcnow() + timedelta(minutes=240),
                }, SECRET_KEY, algorithm=ALGORITHM)

            return JsonResponse({
                'message': 'LOGIN_SUCCESS',
                'token'  : flix_access_token
                }, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)


class KakaoLoginView(View):
    def post(self, request):
        try:
            kakao_access_token = request.headers['Authorization']
            kakao_user_info    = KakaoApi(kakao_access_token).get_kakao_user_info()

            User.objects.update_or_create(
                kakao_id    = kakao_user_info['id'],
                signup_type = 'KAKAO',
                password    = '',
                defaults    = {'name': kakao_user_info['kakao_account']['profile']['nickname']}
            )

            user = User.objects.get(kakao_id=kakao_user_info['id'])
            
            flix_access_token = jwt.encode({
                'user_id'    : user.id,
                'login_type' : 'KAKAO',
                'exp'        : datetime.utcnow() + timedelta(minutes=240),
                }, SECRET_KEY, algorithm=ALGORITHM)

            return JsonResponse({
                'message': 'LOGIN_SUCCESS',
                'token'  : flix_access_token,
            })
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)