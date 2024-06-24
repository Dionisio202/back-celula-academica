from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from .models import CustomUser
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group

class IntegrationTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.group = Group.objects.create(name='Coli')

    def test_register_user(self):
        print("\nRunning test_register_user...")
        user_data = {
            'email': 'test2@example.com',
            'nombre': 'Test',
            'apellido': 'User',
            'cedula': '1234567498',
            'telefono': '1234567898',
            'carrera': 'Test Carrera',
            'semestre': 1,
            'categoria': self.group.id,
            'password': 'password123'
        }

        response = self.client.post('/user/register/', user_data, format='json')
        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['email'], user_data['email'])

    def test_login_user(self):
        print("\nRunning test_login_user...")
        user = CustomUser.objects.create_user(
            email='test@example.com',
            nombre='Test',
            apellido='User',
            cedula='123456789',
            telefono='123456789',
            carrera='Test Carrera',
            semestre=1,
            categoria=self.group,  # Pasamos el objeto Group directamente
            password='password123'
        )

        login_data = {
            'email': 'test@example.com',
            'password': 'password123'
        }

        response = self.client.post('/user/login/', login_data, format='json')
        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['email'], user.email)
