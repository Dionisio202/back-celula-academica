from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from .models import Proyecto
from .serializers import ProyectoSerializer
from django.contrib.auth.models import Group
from users.models import CustomUser
from clubs.models import Club  # Ensure to import your Club model

User = get_user_model()

class RegisterProyectoTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.group = Group.objects.create(name='Secretario')
        cls.user = CustomUser.objects.create_user(
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
        cls.token = Token.objects.create(user=cls.user)
        cls.club = Club.objects.create(
            nombre='Club de Prueba',
            descripcion='Descripción del club de prueba',
            responsable=cls.user
        )
        cls.url = reverse('register_proyecto')

    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_register_proyecto_with_complete_data(self):
        valid_data = {
            'nombre': 'Proyecto de Prueba',
            'descripcion': 'Descripción del proyecto de prueba',
            'fecha_inicio': '2023-05-19',
            'fecha_fin': '2023-12-19',
            'estado': 'En progreso',
            'creador': self.user.id,
            'miembros': [self.user.id],
            'club': self.club.id  # Include the club ID
        }
        response = self.client.post(self.url, valid_data, format='json')
        print(f'\nTest: test_register_proyecto_with_complete_data\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Proyecto.objects.count(), 1)
        self.assertEqual(Proyecto.objects.get().nombre, 'Proyecto de Prueba')

    def test_register_proyecto_with_incomplete_data(self):
        incomplete_data = {
            'nombre': 'Proyecto Incompleto',
            'descripcion': 'Descripción del proyecto incompleto',
        }
        response = self.client.post(self.url, incomplete_data, format='json')
        print(f'\nTest: test_register_proyecto_with_incomplete_data\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Proyecto.objects.count(), 0)


class UpdateProyectoTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.group = Group.objects.create(name='Secretario')
        cls.user = CustomUser.objects.create_user(
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
        cls.token = Token.objects.create(user=cls.user)
        cls.club = Club.objects.create(
            nombre='Club de Prueba',
            descripcion='Descripción del club de prueba',
            responsable=cls.user
        )
        cls.proyecto = Proyecto.objects.create(
            nombre='Proyecto Inicial',
            descripcion='Descripción inicial',
            fecha_inicio='2023-01-01',
            fecha_fin='2023-06-30',
            creador=cls.user,
            club=cls.club  # Ensure the project is associated with the club
        )
        cls.url = reverse('update_proyecto', kwargs={'pk': cls.proyecto.pk})

    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_update_proyecto_with_complete_data(self):
        complete_data = {
            'nombre': 'Proyecto Modificado',
            'descripcion': 'Descripción modificada',
            'fecha_inicio': '2023-02-01',
            'fecha_fin': '2023-07-01'
        }
        response = self.client.put(self.url, complete_data, format='json')
        print(f'\nTest: test_update_proyecto_with_complete_data\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.proyecto.refresh_from_db()
        self.assertEqual(self.proyecto.nombre, 'Proyecto Modificado')
        self.assertEqual(self.proyecto.descripcion, 'Descripción modificada')
        self.assertEqual(str(self.proyecto.fecha_inicio), '2023-02-01')
        self.assertEqual(str(self.proyecto.fecha_fin), '2023-07-01')

    def test_update_proyecto_with_incomplete_data(self):
        incomplete_data = {
            'nombre': ''
        }
        response = self.client.put(self.url, incomplete_data, format='json')
        print(f'\nTest: test_update_proyecto_with_incomplete_data\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.proyecto.refresh_from_db()
        self.assertNotEqual(self.proyecto.nombre, '')
