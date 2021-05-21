from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from .models import *


# Create your tests here.


class TestLoginPost(APITestCase):
    def setUp(self):
        self.url = reverse('login')
        User.objects.create_user('ruslan', None, '12345678')

    def test_login_post(self):
        data = {
            "username": "ruslan",
            "password": "12345678"
        }
        self.response = self.client.post(self.url, data)
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_login_F_password_post(self):
        data = {
            "username": "ruslan",
            "password": "12345670"
        }
        self.response = self.client.post(self.url, data)
        self.assertNotEqual(self.response.status_code, status.HTTP_200_OK)

    def test_login_F_name_post(self):
        data = {
            "username": "ruslan1",
            "password": "12345678"
        }
        self.response = self.client.post(self.url, data)
        self.assertNotEqual(self.response.status_code, status.HTTP_200_OK)


class Test_Dossier_Request(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('dossier')
        self.user = User.objects.create_user('ruslan', None, '12345678')
        self.dossier = Dossier.objects.create(full_name='ruslan sultangaziev', date_birth='2020-02-20', image=None,
                                              gender="M",
                                              user=self.user)
        Car.objects.create(dossier=self.dossier, mark='check_mark', model='check_model', year='2021-02-02', number=1,
                           color='color_check', type='mazda')

    def test_dossier_put(self):
        self.client.login(username='ruslan', password='12345678')
        data = {
            "id": 17,
            "full_name": "Aliy Nurlanova",
            "date_birth": "2021-05-19",
            "gender": "M",
            "user": 1,
            "car": [
                {
                    "car_id": 1,
                    "mark": "mark",
                    "model": "model",
                    "year": "2021-05-21",
                    "number": 2,
                    "color": "color",
                    "type": "mazda"
                }
            ],
            "education": [],
            "warcraft": []
        }
        self.response = self.client.put(self.url, data, format='json')
        print(self.response.json())
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        self.client.login(username='ruslan', password='12345678')
        self.response = self.client.delete(self.url)
        print(self.response.json())
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
