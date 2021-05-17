from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient


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
