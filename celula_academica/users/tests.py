from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from .views import Register

class RegisterTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_register_success(self):
         url = '/api/register/'
         data = {
             'email': 'test1@example.com',
             'password': 'securepassword',
             'name': 'John',
             'lastName': 'Doe'
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
            'email': 'solisedison@outlook.com'
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
            'email': 'solisedison@outlook.com',
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