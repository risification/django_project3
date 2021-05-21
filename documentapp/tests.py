from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User, Group
from .factory import *
from .models import Document


# Create your tests here.


class TestDocumentRulesGet(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('documents-list')
        populate_test_db_users(User, Group)
        populate_test_db_docs(Document)

    def test_serjant_permissions(self):
        self.client.login(username='serjant', password='123456')
        self.response = self.client.get(self.url)
        self.assertContains(self.response, text='private document', status_code=200)

    def test_serjangt_no_permission(self):
        self.client.login(username='serjant', password='123456')
        self.response = self.client.get(self.url)
        self.assertNotContains(self.response, text='secret document', status_code=200)

    def test_general_permission(self):
        self.client.login(username='general', password='123456')
        self.response = self.client.get(self.url)
        self.assertContains(self.response, text='secret document', status_code=200)

    def test_general_no_permission(self):
        self.client.login(username='general', password='123456')
        self.response = self.client.get(self.url)
        self.assertNotContains(self.response, text='top-secret document', status_code=200)

    def test_user_permission(self):
        self.client.login(username='common', password='123456')
        self.response = self.client.get(self.url)
        self.assertContains(self.response, text='public document', status_code=200)

    def test_user_no_permission(self):
        self.client.login(username='common', password='123456')
        self.response = self.client.get(self.url)
        self.assertNotContains(self.response, text='private document', status_code=200)

    def test_president_permission(self):
        self.client.login(username='president', password='123456')
        self.response = self.client.get(self.url)
        self.assertContains(self.response, text='secret document', status_code=200)

    def test_president_top_document_permission(self):
        self.client.login(username='president', password='123456')
        self.response = self.client.get(self.url)
        self.assertContains(self.response, text='top-secret document', status_code=200)


class TestPostDocument(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('documents-list')
        populate_test_db_users(User, Group)

    def test_user_post(self):
        self.client.login(username='common', password='123456')
        data = {
            "title": "test_title",
            "text": "test_text",
            "date_expired": "2020-05-07",
            "status": "active",
            "document_root": "public"
        }
        self.response = self.client.post(self.url, data)
        self.assertNotEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_serjant_post(self):
        self.client.login(username='serjant', password='123456')
        data = {
            "title": "test_title",
            "text": "test_text",
            "date_expired": "2020-05-07",
            "status": "active",
            "document_root": "private"
        }
        self.response = self.client.post(self.url, data)
        self.assertNotEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_general_post(self):
        self.client.login(username='general', password='123456')
        data = {
            "title": "test_title",
            "text": "test_text",
            "date_expired": "2020-05-07",
            "status": "active",
            "document_root": "secret"
        }
        self.response = self.client.post(self.url, data)
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_president_post(self):
        self.client.login(username='president', password='123456')
        data = {
            "title": "test_title",
            "text": "test_text",
            "date_expired": "2020-05-07",
            "status": "active",
            "document_root": "top-secret"
        }
        self.response = self.client.post(self.url, data)
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_general_create_error(self):
        self.client.login(username='general', password='123456')
        data = {
            "title": "test_title",
            "text": "test_text",
            "date_expired": "2020-05-07",
            "status": "active",
            "document_root": "top-secret"
        }
        self.response = self.client.post(self.url, data)
        self.assertContains(self.response, text='You have no permissions!', status_code=400)

    def test_president_create(self):
        self.client.login(username='president', password='123456')
        data = {
            "title": "test_title",
            "text": "test_text",
            "date_expired": "2020-05-07",
            "status": "active",
            "document_root": "top-secret"
        }
        self.response = self.client.post(self.url, data)
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)


class TestDateExpiredDocument(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.doc1 = Document.objects.create(title='not expired doc',
                                            date_expired="2021-12-31", document_root='private')
        self.doc2 = Document.objects.create(title='expired doc',
                                            date_expired="2021-05-09", document_root='private', status='dead')
        populate_test_db_users(User, Group)

    def test_get_not_expired(self):
        self.url = reverse('documents-detail', kwargs={'pk': self.doc1.id})
        self.client.login(username='general', password='123456')
        self.response = self.client.get(self.url)
        print(self.response.json())
        self.assertContains(self.response, 'active', status_code=200)

    def test_get_expired(self):
        self.url = reverse('documents-detail', kwargs={'pk': self.doc2.id})
        self.client.login(username='general', password='123456')
        self.response = self.client.get(self.url)
        print(self.response.json())
        self.assertContains(self.response, 'Страница не найдена', status_code=404)
