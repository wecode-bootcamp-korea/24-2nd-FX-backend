import json

from unittest import mock
from unittest.mock import MagicMock, patch

from django.http import JsonResponse
from django.test import TestCase, Client


class GoogleLoginTest(TestCase):
    def test_google_login_success(self):
        client = Client()
        user = {
            'google_id' : 123456,
            'name'   : 'test_access_token'
        }

        headers   = {'HTTP_Authorization' : 'test_google_access_token'}
        response = client.post('/users/google-login', json.dumps(user), content_type='application/json', **headers)
        result = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),{
                             'message'     : 'LOGIN_SUCCESS',
                             'token'       : result['token'],
                             })

    def test_google_login_success(self):
        client = Client()
        user = {
            'google_id' : 123456,
            'id'   : 'wrong_key'
        }

        headers   = {'HTTP_Authorization' : 'test_google_access_token'}
        response = client.post('/users/google-login', json.dumps(user), content_type='application/json', **headers)
        result = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{
                             'message'     : 'KEY_ERROR',
                             })