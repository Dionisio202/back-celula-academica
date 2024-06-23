import pytest
from django.test import TestCase
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework import status
from .views import register, login, update_user
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from users.models import CustomUser
from users.serializers import UserSerializer

User = get_user_model()


class RegisterViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.group = Group.objects.create(name='Normal')

    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.url = '/user/register/'
        self.valid_data = {
            "email": "juanaz@gmail.com",
            "password": "12345678",
            "nombre": "Juana",
            "apellido": "Perez",
            "cedula": "1805033756",
            "telefono": "099783456",
            "carrera": "Software",
            "semestre": 4,
            "categoria": self.group.id
        }

    def test_register_with_valid_data(self):
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_with_null_data(self):
        null_data = {
            "email": None,
            "password": None,
            "nombre": None,
            "apellido": None,
            "cedula": None,
            "telefono": None,
            "carrera": None,
            "semestre": None,
            "categoria": None
        }
        response = self.client.post(self.url, null_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_blank_data(self):
        blank_data = {
            "email": "",
            "password": "",
            "nombre": "",
            "apellido": "",
            "cedula": "",
            "telefono": "",
            "carrera": "",
            "semestre": "",
            "categoria": ""
        }
        response = self.client.post(self.url, blank_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_invalid_data(self):
        invalid_data = {
            "email": "invalid_email",
            "password": "short",
            "nombre": "Juan",
            "apellido": "Perez",
            "cedula": "invalid_cedula",
            "telefono": "invalid_phone",
            "carrera": "Software",
            "semestre": "invalid_semestre",
            "categoria": self.group.id
        }
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_repeated_data(self):
        self.client.post(self.url, self.valid_data, format='json')

        repeated_data = {
            "email": "juanaz@gmail.com",
            "password": "12345678",
            "nombre": "Juan",
            "apellido": "Perez",
            "cedula": "1805033726",
            "telefono": "099783456",
            "carrera": "Software",
            "semestre": 4,
            "categoria": self.group.id
        }

        response = self.client.post(self.url, repeated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.group = Group.objects.create(name='Colider')
        cls.user = User.objects.create_user(
            email='test@example.com',
            password='12345678',
            nombre='Test',
            apellido='User',
            cedula='1805033726',
            telefono='099783456',
            carrera='Software',
            semestre=4,
            categoria=cls.group
        )

    def setUp(self):
        self.client = APIClient()
        self.url = '/user/login/'

    def test_login_with_existing_credentials(self):
        login_data = {
            "email": "test@example.com",
            "password": "12345678"
        }
        response = self.client.post(self.url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_invalid_credentials(self):
        login_data = {
            "email": "test@example.com",
            "password": "invalid_password"
        }
        response = self.client.post(self.url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_inactive_user(self):
        self.user.is_active = False
        self.user.save()

        login_data = {
            "email": "test@example.com",
            "password": "12345678"
        }
        response = self.client.post(self.url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateUserViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.group = Group.objects.create(name='Administrador')
        cls.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='12345678',
            nombre='Test',
            apellido='User',
            cedula='1805033726',
            telefono='099783456',
            carrera='Software',
            semestre=4,
            categoria=cls.group
        )
        cls.token = Token.objects.create(user=cls.user)

    def setUp(self):
        self.client = APIClient()
        self.url = '/user/update_user/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_update_user_with_valid_data(self):
        update_data = {
            "email": "updated@example.com",
            "nombre": "Updated",
            "apellido": "User Updated",
            "cedula": "1805033728",
            "telefono": "099783458",
            "carrera": "Updated Software",
            "semestre": 5,
            "categoria": self.group.id
        }
        response = self.client.put(self.url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_with_empty_fields(self):
        empty_data = {
            "email": "",
            "nombre": "",
            "apellido": "",
            "cedula": "",
            "telefono": "",
            "carrera": "",
            "semestre": "",
            "categoria": self.group.id
        }
        response = self.client.put(self.url, empty_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_update_user_with_duplicate_email(self):
        duplicate_email_data = {
            "email":"updated@example.com",
            "cedula":"1850085364",
            "telefono":"0983860122",
            "carrera":"Software",
            "semestre":6,
            "password":'123456',
            "nombre":'Edison',
            "apellido":'Ortiz',
            "categoria": self.group.id
        }
        response = self.client.put(self.url, duplicate_email_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

  

class SearchUserViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.group = Group.objects.create(name='Secretario')
        cls.user1 = CustomUser.objects.create_user(
            email='user1@example.com',
            password='12345678',
            nombre='John',
            apellido='Doe',
            cedula='1805033726',
            telefono='099783456',
            carrera='Software',
            semestre=4,
            categoria=cls.group
        )
        cls.user2 = CustomUser.objects.create_user(
            email='user2@example.com',
            password='12345678',
            nombre='Jane',
            apellido='Doe',
            cedula='1805033727',
            telefono='099783457',
            carrera='Software',
            semestre=5,
            categoria=cls.group
        )
        cls.token = Token.objects.create(user=cls.user1)

    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = '/user/search_user/'

    def test_search_user_with_existing_data(self):
        response = self.client.get(self.url, {'nombre': 'John'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(self.url, {'cedula': '1805033727'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_user_with_non_existing_data(self):
        response = self.client.get(self.url, {'nombre': 'Nonexistent'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.get(self.url, {'cedula': '0000000000'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_search_user_without_parameters(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
