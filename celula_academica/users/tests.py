from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from .views import Register

class RegisterTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_register_success(self):
        url = '/api/register/?email=testys@example.com&password=securepassword&name=John&lastName=Doe'
        request = self.factory.post(url)
        view = Register.as_view()
        response = view(request)

        # Verifica que la respuesta tenga el código 200 (éxito)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('Registrado con exito', response.data)

    def test_register_missing_data(self):
        url = '/api/register/?email=solisedison@outlook.com'
        request = self.factory.post(url)
        view = Register.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('Debes proporcionar un correo electrónico y una contraseña', response.data['error'])

    def test_register_exceded(self):
        url = '/api/register/?email=testiess@example.com&password=securepassword&name=John&lastName=Doe'
        request = self.factory.post(url)
        view = Register.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

        self.assertIn('Limite de registros excedidos', response.data)

