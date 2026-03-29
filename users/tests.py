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

@pytest.mark.django_db
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
            "telefono": "0997834569",
            "carrera": "Software",
            "semestre": 4,
            "categoria": self.group.id
        }

    def test_register_with_valid_data(self):
        print("\nRunning test_register_with_valid_data...")
        response = self.client.post(self.url, self.valid_data, format='json')
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_with_null_data(self):
        print("\nRunning test_register_with_null_data...")
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
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_blank_data(self):
        print("\nRunning test_register_with_blank_data...")
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
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_invalid_data(self):
        print("\nRunning test_register_with_invalid_data...")
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
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_repeated_data(self):
        print("\nRunning test_register_with_repeated_data...")
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
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@pytest.mark.django_db
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
        print("\nRunning test_login_with_existing_credentials...")
        login_data = {
            "email": "test@example.com",
            "password": "12345678"
        }
        response = self.client.post(self.url, login_data, format='json')
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_invalid_credentials(self):
        print("\nRunning test_login_with_invalid_credentials...")
        login_data = {
            "email": "test@example.com",
            "password": "invalid_password"
        }
        response = self.client.post(self.url, login_data, format='json')
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_inactive_user(self):
        print("\nRunning test_login_with_inactive_user...")
        self.user.is_active = False
        self.user.save()

        login_data = {
            "email": "test@example.com",
            "password": "12345678"
        }
        response = self.client.post(self.url, login_data, format='json')
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@pytest.mark.django_db
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
        print("\nRunning test_update_user_with_valid_data...")
        update_data = {
            "email": "updated@example.com",
            "nombre": "Updated",
            "apellido": "User Updated",
            "cedula": "1805033728",
            "telefono": "0997834587",
            "carrera": "Updated Software",
            "semestre": 5,
            "categoria": self.group.id
        }
        response = self.client.put(self.url, update_data, format='json')
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_with_empty_fields(self):
        print("\nRunning test_update_user_with_empty_fields...")
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
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user_with_duplicate_email(self):
        print("\nRunning test_update_user_with_duplicate_email...")
        duplicate_email_data = {
            "email": "updated@example.com",
            "cedula": "1850085364",
            "telefono": "0983860122",
            "carrera": "Software",
            "semestre": 6,
            "password": '123456',
            "nombre": 'Edison',
            "apellido": 'Ortiz',
            "categoria": self.group.id
        }
        response = self.client.put(self.url, duplicate_email_data, format='json')
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@pytest.mark.django_db
class SearchUserViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.group = Group.objects.create(name='Secretario')
        cls.user1 = CustomUser.objects.create_user(
            email='user7@example.com',
            password='12345678',
            nombre='User1',
            apellido='One',
            cedula='1805033726',
            telefono='099783456',
            carrera='Software',
            semestre=4,
            categoria=cls.group
        )
        cls.user2 = CustomUser.objects.create_user(
            email='user2@example.com',
            password='12345678',
            nombre='User2',
            apellido='Two',
            cedula='1805033727',
            telefono='0997834578',
            carrera='Software',
            semestre=5,
            categoria=cls.group
        )
        cls.token = Token.objects.create(user=cls.user1)

    def setUp(self):
        self.client = APIClient()
        self.url = '/user/search_user/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    # def test_search_user_with_valid_query(self):
    #     print("\nRunning test_search_user_with_valid_query...")
    #     response = self.client.get(self.url, {'search': 'Test'})
    #     print(f"Response status code: {response.status_code}")
    #     print(f"Response content: {response.content}")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_user_with_empty_query(self):
        print("\nRunning test_search_user_with_empty_query...")
        response = self.client.get(self.url, {'search': ''})
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
