# Create your tests here.
# Hacer los tests del login
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from .views import Login

class LoginTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_login_success(self):
        url = '/api/login/'
        data = {
            'email': 'solisedison@outlook.com',
            'password': '123456'
        }
        request = self.factory.post(url, data)
        view = Login.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)


    def test_login_missing_data(self):
        url = '/api/login/'
        data = {'email': 'test@example.com'}
        request = self.factory.post(url, data)
        view = Login.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'Debes proporcionar un correo electrónico y una contraseña')

    def test_login_invalid_credentials(self):
        url = '/api/login/'
        data = {
            'email': 'invalid@correo.com',
            'password': 'invalidpassword'
        }
        request = self.factory.post(url, data)
        view = Login.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'invalid_grant')

    def test_login_empty_fields(self):
        url = '/api/login/'
        data = {'email': '', 'password': ''}
        request = self.factory.post(url, data)
        view = Login.as_view()
        response = view(request)

        self.assertIn(response.status_code, [400, 401])
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Debes proporcionar un correo electrónico y una contraseña')


