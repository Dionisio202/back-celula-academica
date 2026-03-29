from django.test import TestCase, Client
from rest_framework import status
from django.urls import reverse
from .models import Club, Proyecto, CustomUser
from django.contrib.auth.models import Group

class ClubProyectoIntegrationTest(TestCase):

    def setUp(self):
        self.client = Client()

        # Create a group for categoria field
        group = Group.objects.create(name='test_group')

        # Create a user and log in
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            nombre='Test',
            apellido='User',
            cedula='1234567890',
            telefono='0987654321',
            carrera='Ingeniería',
            semestre=1,
            categoria=group,
            password='testpassword'
        )
        self.client.login(email='testuser@example.com', password='testpassword')

        # Define data
        self.club_data = {
            'nombre': 'Club Test',
            'descripcion': 'Descripción del Club Test',
            'responsable': self.user.id
        }

        self.proyecto_data = {
            'nombre': 'Proyecto Test',
            'descripcion': 'Descripción del Proyecto Test',
            'club': None  # Este será asignado después de crear un club
        }

    def test_create_club(self):
        response = self.client.post(reverse('club-list-create'), self.club_data, content_type='application/json')
        print(f'\nTest: test_create_club\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nombre'], self.club_data['nombre'])

    def test_create_proyecto(self):
        # Create a club first
        club = Club.objects.create(
            nombre=self.club_data['nombre'],
            descripcion=self.club_data['descripcion'],
            responsable=self.user  # Pass the user instance
        )
        self.proyecto_data['club'] = club.id  # Use id for API request

        response = self.client.post(reverse('proyecto-list-create'), self.proyecto_data, content_type='application/json')
        print(f'\nTest: test_create_proyecto\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nombre'], self.proyecto_data['nombre'])

    def test_get_clubs(self):
        Club.objects.create(
            nombre=self.club_data['nombre'],
            descripcion=self.club_data['descripcion'],
            responsable=self.user  # Pass the user instance
        )
        response = self.client.get(reverse('club-list-create'), format='json')
        print(f'\nTest: test_get_clubs\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nombre'], self.club_data['nombre'])

    def test_get_proyectos(self):
        # Create a club and a project
        club = Club.objects.create(
            nombre=self.club_data['nombre'],
            descripcion=self.club_data['descripcion'],
            responsable=self.user  # Pass the user instance
        )
        self.proyecto_data['club'] = club.id  # Use id for API request
        Proyecto.objects.create(
            nombre=self.proyecto_data['nombre'],
            descripcion=self.proyecto_data['descripcion'],
            club=club  # Pass the club instance
        )

        response = self.client.get(reverse('proyecto-list-create'), format='json')
        print(f'\nTest: test_get_proyectos\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nombre'], self.proyecto_data['nombre'])
