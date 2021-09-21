from django.test import TestCase, Client

from .models import Content, Genre, Detail, ContentGenre

class ContentTest(TestCase):
    def setUp(self):
        Genre.objects.create(
            id = 1,
            name = "drama"
        )
        Genre.objects.create(
            id = 2,
            name = "action"
        )
        Genre.objects.create(
            id = 3,
            name = "comedy"
        )

        Content.objects.create(
            id = 1,
            name = "The war",
            category = "movie",
            description = "good movie",
            nation = "UK",
            thumb_nail = "www.naver.com"
        )

        Content.objects.create(
            id = 2,
            name = "Harry Potter",
            category = "drama",
            description = "good movie",
            nation = "UK",
            thumb_nail = "www.naver.com"
        )

        Detail.objects.create(
            id = 1,
            episode = "Harry Potter and the Philosopher(Sorcerer)'s Stone",
            description = "best episode",
            running_time = "120",
            thumb_nail = "www.wecode.com",
            file = "www.ewcode.com",
            content = Content.objects.get(id=2)
        )

        Detail.objects.create(
            id = 2,
            episode = "The war first episode",
            description = "best episode",
            running_time = "140",
            thumb_nail = "www.wecode.com",
            file = "www.ewcode.com",
            content = Content.objects.get(id=1)
        )

        Detail.objects.create(
            id = 3,
            episode = "The war second episode",
            description = "best episode2",
            running_time = "150",
            thumb_nail = "www.wecode.com",
            file = "www.ewcode.com",
            content = Content.objects.get(id=1)
        )

        ContentGenre.objects.create(
            id = 1,
            content = Content.objects.get(id=1),
            genre = Genre.objects.get(id=1)
        )

        ContentGenre.objects.create(
            id = 2,
            content = Content.objects.get(id=1),
            genre = Genre.objects.get(id=2)
        )

        ContentGenre.objects.create(
            id = 3,
            content = Content.objects.get(id=2),
            genre = Genre.objects.get(id=2)
        )

        ContentGenre.objects.create(
            id = 4,
            content = Content.objects.get(id=2),
            genre = Genre.objects.get(id=3)
        )

    def tearDown(self):
        Content.objects.all().delete()
        Genre.objects.all().delete()
        Detail.objects.all().delete()
        ContentGenre.objects.all().delete()
    
    def test_content_get_success(self):
        client   = Client()
        response = client.get('/content/1')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "Result": {
            "id": 1,
            "name": "The war",
            "category": "movie",
            "description": "good movie",
            "nation": "UK",
            "thumb_nail": "www.naver.com",
            "genre": [
                {
                    "genre": "drama"
                },
                {
                    "genre": "action"
                }
            ],
            "detail": [
                {
                    "episode": "The war first episode",
                    "detail_description": "best episode",
                    "running_time": 140,
                    "detail_thumb_nail": "www.wecode.com"
                },
                {
                    "episode": "The war second episode",
                    "detail_description": "best episode2",
                    "running_time": 150,
                    "detail_thumb_nail": "www.wecode.com"
                    },
            ]
            }
        })


    def test_content_get_dose_not_exist_content(self):
        client   = Client()
        response = client.get('/content/3')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"Result": "CONTENT_DOES_NOT_EXIST"})

    
    def test_contentlist_get_success(self):
        client   = Client()
        response = client.get('/content/list?limit=2&order-by=id')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
        {
            "Result": [
                {
                    "id": 1,
                    "name": "The war",
                    "category": "movie",
                    "description": "good movie",
                    "nation": "UK",
                    "thumb_nail": "www.naver.com",
                    "genre": [
                        {
                            "genre": "drama"
                        },
                        {
                            "genre": "action"
                        }
                    ]
                },
                {
                    "id": 2,
                    "name": "Harry Potter",
                    "category": "drama",
                    "description": "good movie",
                    "nation": "UK",
                    "thumb_nail": "www.naver.com",
                    "genre": [
                        {
                            "genre": "action"
                        },
                        {
                            "genre": "comedy"
                        }
                    ]
                }
                ]
        })

    def test_contentlist_get_field_error(self):
        client   = Client()
        response = client.get('/content/list?order-by=hott')
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"Result": "FIELD_ERROR"})

    def test_contentlist_get_dose_not_exist_content(self):
        client   = Client()
        response = client.get('/content/list?category=acction')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"Result": []})