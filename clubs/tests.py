from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Club
from users.models import CustomUser
from django.contrib.auth.models import Group

class ClubListCreateAPIViewTest(APITestCase):
    def setUp(self):
        self.group = Group.objects.create(name='TestGroup')
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            nombre='Test',
            apellido='User',
            cedula='1234567890',
            telefono='1234567890',
            carrera='Informatica',
            semestre=5,
            categoria=self.group
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('club-list-create')
        self.club_data = {
            'nombre': 'Club de Prueba',
            'descripcion': 'Descripción del club de prueba',
            'responsable': self.user.id,
        }

    def test_create_club(self):
        response = self.client.post(self.url, self.club_data, format='json')
        print(f'\nTest: test_create_club\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Club.objects.count(), 1)
        self.assertEqual(Club.objects.get().nombre, 'Club de Prueba')

    def test_get_clubs(self):
        Club.objects.create(
            nombre=self.club_data['nombre'],
            descripcion=self.club_data['descripcion'],
            responsable=self.user  # Assign the CustomUser instance here
        )
        response = self.client.get(self.url)
        print(f'\nTest: test_get_clubs\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nombre'], 'Club de Prueba')


class ClubRetrieveUpdateDestroyAPIViewTest(APITestCase):
    def setUp(self):
        self.group = Group.objects.create(name='TestGroup')
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            nombre='Test',
            apellido='User',
            cedula='1234567890',
            telefono='1234567890',
            carrera='Informatica',
            semestre=5,
            categoria=self.group
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.club = Club.objects.create(
            nombre='Club de Prueba',
            descripcion='Descripción del club de prueba',
            responsable=self.user
        )
        self.url = reverse('club-detail', kwargs={'pk': self.club.pk})

    def test_get_club(self):
        response = self.client.get(self.url)
        print(f'\nTest: test_get_club\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Club de Prueba')

    def test_update_club(self):
        updated_data = {
            'nombre': 'Club Actualizado',
            'descripcion': 'Descripción actualizada',
            'responsable': self.user.id,
        }
        response = self.client.put(self.url, updated_data, format='json')
        print(f'\nTest: test_update_club\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.club.refresh_from_db()
        self.assertEqual(self.club.nombre, 'Club Actualizado')

    def test_partial_update_club(self):
        updated_data = {'nombre': 'Club Parcialmente Actualizado'}
        response = self.client.patch(self.url, updated_data, format='json')
        print(f'\nTest: test_partial_update_club\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.club.refresh_from_db()
        self.assertEqual(self.club.nombre, 'Club Parcialmente Actualizado')

    def test_delete_club(self):
        response = self.client.delete(self.url)
        print(f'\nTest: test_delete_club\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Club.objects.filter(pk=self.club.pk).exists())
