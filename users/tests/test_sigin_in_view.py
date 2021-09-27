import json
from unittest import mock
from unittest.mock import MagicMock, patch

from django.http import response
from django.test import TestCase, Client

from users.models import User


class SignInTest(TestCase):
    def setUp(self):
        User.objects.create(
            name        = 'Mark 1',
            email       = 'Mark1@stark.com',
            password    = '$2b$12$XwtwesAaItrhXqS95DtjRuLcz/MxzWluKXrrWkezkiP.eTnZvGhI2',
            signup_type = 'FLIX'
        )

    def tearDown(self):
        User.objects.all().delete()

    @patch('requests.post')
    def test_signinview_post_success(self, mocked_requests):
        client = Client()
        user = {
            'email'       : 'Mark1@stark.com',
            'password'    : 'test1234**',
            'signup_type' : 'FLIX'
        }
        class MockedResponse:
            def json(self):
                return {
                    'message': 'LOGIN_SUCCESS',
                    'token'  : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.bm4G8wIigOyF9JqbQnAEfOF-O3i74mi6XRH_ojkdo-U'
                }
        mocked_requests.post = MagicMock(return_value=MockedResponse())
        response = client.post('/users/sign-in', json.dumps(user), content_type='application/json')
 
        self.assertEqual(response.status_code, 200)
    
    def test_signinview_post_unregistered_user(self):
        client = Client()
        user = {
            'email'       : 'Mark123456@stark.com',
            'password'    : 'test1234**',
            'signup_type' : 'FLIX'
        }
        response = client.post('/users/sign-in', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'message' : 'USER_DOES_NOT_EXIST'
        })

    def test_signinview_post_invalid_password(self):
        client = Client()
        user = {
            'email'       : 'Mark1@stark.com',
            'password'    : 'testtest11223344***',
            'signup_type' : 'FLIX'
        }
        response = client.post('/users/sign-in', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {
            'message': 'INVALID_PASSWORD'
        })

    def test_signinview_post_invalid_keys(self):
        client = Client()
        user = {
            'email'       : 'Mark1@stark.com',
            'pass'        : 'test1234**',
            'signup_type' : 'FLIX'
        }
        response = client.post('/users/sign-in', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'message': 'KEY_ERROR'
        })

    def test_signinview_post_not_flix_type_login(self):
        client = Client()
        user = {
            'email'       : 'Mark1@stark.com',
            'pass'        : 'test1234**',
            'signup_type' : 'KAKAO'
        }
        response = client.post('/users/sign-in', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'message': 'LOGIN_TYPE_IS_NOT_FLIX'
        })

