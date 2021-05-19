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

    def test_dossier_put(self):
        self.client.login(username='ruslan', password='12345678')
        data = {
            "full_name": "ruslan sultangaziev112",
            "date_birth": "2021-05-19",
            "gender": "M",
            "user": 1,
            "car": [],
            "education": [],
            "warcraft": []
        }
        self.response = self.client.put(self.url, data)
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_delete(self):
        self.client.login(username='ruslan', password='12345678')
        self.response = self.client.delete(self.url)
        print(self.response.json())
        self.assertEqual(self.response.status_code,status.HTTP_200_OK)
