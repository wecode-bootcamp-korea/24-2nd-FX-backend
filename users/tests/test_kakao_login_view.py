import jwt
import json
from unittest import mock
from unittest.mock import MagicMock, patch

from django.http import cookie, response
from django.db import transaction
from django.test import TestCase, Client, client

from users.models import User
from my_settings import SECRET_KEY, ALGORITHM


class KakaoLoginTest(TestCase):
    @patch('users.views.requests')
    def test_kakao_login_success(self, mocked_requests):
        client    = Client()

        class MockedResponse:
            def json(self):
                return {
                    'id': 1235,
                    'kakao_account': {
                        'profile'  : {
                            'nickname': 'test'
                        }
                    }
                }
        mocked_requests.get = MagicMock(return_value = MockedResponse())

        headers   = {'HTTP_Authorization' : 'test_kakao_access_token'}
        response = client.post('/users/kakao-login', content_type='application/json', **headers)
        result = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),{
                             'message'     : 'LOGIN_SUCCESS',
                             'token'       : result['token'],
                             })

    def test_kakao_login_key_error(self):
        client = Client()

        headers  = {'key_error_header': 'test_kakao_access_token',}
        response = client.post('/users/kakao-login', content_type='application/json', **headers)

        self. assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
                            'message': 'KEY_ERROR',
                            })

