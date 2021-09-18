import json
import jwt
from datetime import datetime, timedelta

from django.test import TestCase, Client

from .models import Wishlist
from contents.models import Content
from users.models import User
from .views import WishListView
from my_settings import ALGORITHM, SECRET_KEY

class ContentTest(TestCase):
    def setUp(self):
        User.objects.create(
            id          = 1,
            name        = "test",
            email       = "test@gamil.com",
            password    = "1q2w3e4r!",
            signup_type = "kakao",
            kakao_id    = "test",
        )

        User.objects.create(
            id          = 2,
            name        = "test2",
            email       = "test2@gamil.com",
            password    = "1q2w3e4r!",
            signup_type = "kakao",
            kakao_id    = "test2",
        )

        Content.objects.create(
            id          = 1,
            name        = "The war",
            category    = "movie",
            description = "good movie",
            nation      = "UK",
            thumb_nail  = "www.naver.com"
        )

        Content.objects.create(
            id          = 2,
            name        = "The war2",
            category    = "movie",
            description = "good movie2",
            nation      = "UK",
            thumb_nail  = "www.naver.com"
        )

        Wishlist.objects.create(
            id = 2,
            user_id = 2,
            content_id = 2,
            like = True
        )

    def tearDown(self):
        Content.objects.all().delete()
        User.objects.all().delete()
        Wishlist.objects.all().delete()


    def test_create_wishlist(self):
        content      = {"content_id" : 1}
        access_token = jwt.encode({
                'user_id': 1,
                'exp'    : datetime.utcnow() + timedelta(minutes=10)
                }, SECRET_KEY, algorithm=ALGORITHM)

        client   = Client()
        header   = {"HTTP_Authorization" : access_token}
        response = client.patch('/wishlists', json.dumps(content), **header, content_type='application/json')

        self.assertEqual(response.status_code, 206)
        self.assertEqual(response.json(), {
            "Result": {
            "user_id": 1,
            "content_id": 1,
            "like": True,
            }})


    def test_toggle_wishlist(self):
        content      = {"content_id" : 2}
        access_token = jwt.encode({
                'user_id': 2,
                'exp'    : datetime.utcnow() + timedelta(minutes=10)
                }, SECRET_KEY, algorithm=ALGORITHM)

        client   = Client()
        header   = {"HTTP_Authorization" : access_token}
        response = client.patch('/wishlists', json.dumps(content), **header, content_type='application/json')

        self.assertEqual(response.status_code, 206)
        self.assertEqual(response.json(), {
            "Result": {
            "user_id": 2,
            "content_id": 2,
            "like": False,
            }})


    def test_content_get_dose_not_exist_content(self):
        content      = {"content_id" : 3}
        access_token = jwt.encode({
                'user_id': 1,
                'exp'    : datetime.utcnow() + timedelta(minutes=10)
                }, SECRET_KEY, algorithm=ALGORITHM)

        client   = Client()
        header   = {"HTTP_Authorization" : access_token}
        response = client.patch('/wishlists', json.dumps(content), **header, content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"Result": "CONTENT_DOES_NOT_EXIST"})


    def test_jwt_does_not_exist(self):
        content  = {"content_id" : 1}
        client   = Client()
        response = client.patch('/wishlists', json.dumps(content), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'KEY_ERROR'})