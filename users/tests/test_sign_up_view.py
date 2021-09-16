import json
from unittest import mock

from django.http import response
from django.db import transaction
from django.test import TestCase, Client

from users.models import User

class SignUpTest(TestCase):
    def test_signupview_post_success(self):
        client = Client()
        user = {
            'name'        : 'Mark 1',
            'email'       : 'Mark1@stark.com',
            'password'    : 'mark486**',
            'signup_type' : 'flix'
        }
        response = client.post('/users/sign-up', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),{
            'message': 'SUCCESS'
        })

    def test_signupview_post_invalid_email_format(self):
        client = Client()
        user = {
            'name'        : 'Mark 1',
            'email'       : 'Mark1starkcom',
            'password'    : 'mark486**',
            'signup_type' : 'flix'
        }
        response = client.post('/users/sign-up', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{
            'message': 'INVALID_EMAIL_FORMAT'
        })

    def test_signupview_post_invalid_password_format(self):
        client = Client()
        user = {
            'name'        : 'Mark 1',
            'email'       : 'Mark1@stark.com',
            'password'    : 'mark486',
            'signup_type' : 'flix'
        }
        response = client.post('/users/sign-up', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{
            'message': 'INVALID_PASSWORD_FORMAT'
        })

    def test_signupview_post_invalid_keys(self):
        client = Client()
        user = {
            'name'        : 'Mark 1',
            'email'       : 'Mark1@stark.com',
            'password'    : 'mark486**',
        }
        response = client.post('/users/sign-up', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{
            'message': 'KEY_ERROR'
        })

    def setUp(self):
        User.objects.create(
            name = 'Mark 2',
            email = 'Mark2@stark.com',
            password = 'mark486**',
            signup_type = 'flix'
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_signupview_post_duplicated_user(self):
        client = Client()
        user = {
            'name'        : 'Mark 2',
            'email'       : 'Mark2@stark.com',
            'password'    : 'mark486**',
            'signup_type' : 'flix'
        }
        response = client.post('/users/sign-up', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{
            'message': 'USER_ALREADY_EXISTS'
        })

    def test_signupview_post_data_too_long(self):
        client = Client()
        user = {
            'name'        : 'Mark3 is the best in the world hahahahahahahahahahahahahaha',
            'email'       : 'Mark3@stark.com',
            'password'    : 'mark486**',
            'signup_type' : 'flix'
        }
        try:
            with transaction.atomic():
                response = client.post('/users/sign-up', json.dumps(user), content_type='application/json')
        except IntegrityError:
            pass
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{
            'message': 'DATA_TOO_LONG'
        })
