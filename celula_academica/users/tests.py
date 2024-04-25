# Create your tests here.
# Hacer los tests del login
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from .views import Register
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
        self.assertEqual(response.data['error'], 'Credenciales inválidas')

    def test_login_empty_fields(self):
        url = '/api/login/'
        data = {'email': '', 'password': ''}
        request = self.factory.post(url, data)
        view = Login.as_view()
        response = view(request)

        self.assertIn(response.status_code, [400, 401])
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Debes proporcionar un correo electrónico y una contraseña')

###test Register 
class RegisterTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_register_success(self):
          url = '/api/register/'
          data = {
              'email': 'solis@outlook.com',
              'password': '123456',
              'name': 'Edison',
              'lastName': 'Ortiz'
          }
          request = self.factory.post(url, data)
          view = Register.as_view()
          response = view(request)

          # Verifica que la respuesta tenga el código 200 (éxito)
          self.assertEqual(response.status_code, status.HTTP_200_OK)

          self.assertIn('Registrado con éxito', response.data['message'])

    def test_register_missing_data(self):
        url = '/api/register/'
        data = {
            'email': 'solisedin@outlook.com'
        }
        request = self.factory.post(url, data)
        view = Register.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('Debes proporcionar un correo electrónico y una contraseña', response.data['error'])

    # def test_register_exceeded(self):
    #     url = '/api/register/'
    #     data = {
    #         'email': 'testiess@example.com',
    #         'password': 'securepassword',
    #         'name': 'John',
    #         'lastName': 'Doe'
    #     }
    #     for _ in range(5):
    #         request = self.factory.post(url, data)
    #         view = Register.as_view()
    #         response = view(request)

    #     self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    #     self.assertIn('Límite de registros excedidos', response.data['error'])

    def test_register_passwordError(self):
        url = '/api/register/'
        data = {
            'email': 'testiess@example.com',
            'password': '12345',
            'name': 'John',
            'lastName': 'Doe'
        }
        for _ in range(5):
            request = self.factory.post(url, data)
            view = Register.as_view()
            response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('La contraseña debe tener al menos 6 caracteres', response.data['error'])
        
    def test_register_Noname(self):
        url = '/api/register/'
        data = {
            'email': 'testiess@example.com',
            'password': '12345',
            'lastName': 'Doe'
        }
        for _ in range(5):
            request = self.factory.post(url, data)
            view = Register.as_view()
            response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('Debes proporcionar un nombre y un apellido', response.data['error'])

    def test_register_emailExist(self):
        url = '/api/register/'
        data = {
            'email': 'solis@outlook.com',
            'password': '123456',
            'name': 'Edison',
            'lastName': 'Ortiz'
        }
        for _ in range(5):
            request = self.factory.post(url, data)
            view = Register.as_view()
            response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('El correo electrónico ya está registrado', response.data['error'])
