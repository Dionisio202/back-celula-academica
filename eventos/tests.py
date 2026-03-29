from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Concurso, Charla, Ponente
from eventos.models import Ponente, Concurso, InscripcionConcurso
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group
from users.models import CustomUser

# Concurso

class ConcursoListCreateAPIViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('api_concursos_list_create')
        self.concurso_data = {
            'nombre': 'Concurso de Prueba',
            'descripcion': 'Descripción del concurso de prueba',
            'fecha_inicio': '2023-05-19',
            'fecha_fin': '2023-12-19',
            'competencia_individual': True,
            'max_integrantes': 5,
            'valor_inscripcion': '10.00',
        }
        self.client.post(self.url, self.concurso_data, format='json')

    def test_create_concurso(self):
        response = self.client.post(self.url, self.concurso_data, format='json')
        print(f'\nTest: test_create_concurso\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Concurso.objects.count(), 2)

    def test_get_concursos(self):
        response = self.client.get(self.url)
        print(f'\nTest: test_get_concursos\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        self.assertIn(self.concurso_data['nombre'], [concurso['nombre'] for concurso in response.data])


class ConcursoRetrieveUpdateDestroyAPIViewTest(APITestCase):

    def setUp(self):
        self.concurso = Concurso.objects.create(
            nombre='Concurso de Programación',
            descripcion='Descripción del concurso',
            fecha_inicio='2024-07-01',
            fecha_fin='2024-07-05',
            valor_inscripcion=100.00,
            competencia_individual=True
        )

    def test_get_concurso(self):
        url = reverse('api_concursos_detail', kwargs={'pk': self.concurso.pk})
        response = self.client.get(url)
        print(f'\nTest: test_get_concurso\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Concurso de Programación')

    def test_update_concurso(self):
        url = reverse('api_concursos_detail', kwargs={'pk': self.concurso.pk})
        data = {
            'nombre': 'Concurso de Matemáticas',
            'descripcion': 'Descripción actualizada',
            'fecha_inicio': '2024-07-01',
            'fecha_fin': '2024-07-10',
            'valor_inscripcion': 150.00,
            'competencia_individual': True
        }
        response = self.client.put(url, data, format='json')
        print(f'\nTest: test_update_concurso\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.concurso.refresh_from_db()
        self.assertEqual(self.concurso.nombre, 'Concurso de Matemáticas')

    def test_delete_concurso(self):
        url = reverse('api_concursos_detail', kwargs={'pk': self.concurso.pk})
        response = self.client.delete(url)
        print(f'\nTest: test_delete_concurso\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Concurso.objects.filter(pk=self.concurso.pk).exists())

# Charla

class CharlaTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.group = Group.objects.create(name='TestGroup')
        cls.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            nombre='Test',
            apellido='User',
            cedula='1234567890',
            telefono='1234567890',
            carrera='Informatica',
            semestre=5,
            categoria=cls.group
        )
        cls.token = Token.objects.create(user=cls.user)
        cls.ponente1 = Ponente.objects.create(nombre='Ponente 1')
        cls.ponente2 = Ponente.objects.create(nombre='Ponente 2')
        cls.charla = Charla.objects.create(
            nombre='Charla 1',
            descripcion='Descripción de prueba',
            fecha_inicio='2023-06-23',
            fecha_fin='2023-06-24'
        )
        cls.charla.ponentes.set([cls.ponente1, cls.ponente2])
        cls.charla.save()
        cls.charla_url = reverse('api_charlas_list_create')
        cls.charla_detail_url = reverse('api_charlas_detail', kwargs={'pk': cls.charla.pk})

    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_charla(self):
        data = {
            'nombre': 'Nueva Charla',
            'descripcion': 'Descripción de la nueva charla',
            'fecha_inicio': '2023-06-24',
            'fecha_fin': '2023-06-25',
            'ponentes': [self.ponente1.id, self.ponente2.id]
        }
        response = self.client.post(self.charla_url, data, format='json')
        print(f'\nTest: test_create_charla\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Charla.objects.count(), 2)
        self.assertEqual(Charla.objects.get(id=response.data['id']).nombre, 'Nueva Charla')

    def test_retrieve_charla(self):
        response = self.client.get(self.charla_detail_url)
        print(f'\nTest: test_retrieve_charla\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], self.charla.nombre)

    def test_update_charla(self):
        data = {
            'nombre': 'Charla Actualizada',
            'descripcion': 'Descripción actualizada',
            'fecha_inicio': '2023-06-25',
            'fecha_fin': '2023-06-26',
            'ponentes': [self.ponente1.id]
        }
        response = self.client.put(self.charla_detail_url, data, format='json')
        print(f'\nTest: test_update_charla\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.charla.refresh_from_db()
        self.assertEqual(self.charla.nombre, 'Charla Actualizada')

    def test_partial_update_charla(self):
        data = {
            'nombre': 'Charla Parcialmente Actualizada'
        }
        response = self.client.patch(self.charla_detail_url, data, format='json')
        print(f'\nTest: test_partial_update_charla\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.charla.refresh_from_db()
        self.assertEqual(self.charla.nombre, 'Charla Parcialmente Actualizada')

    def test_delete_charla(self):
        response = self.client.delete(self.charla_detail_url)
        print(f'\nTest: test_delete_charla\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Charla.objects.count(), 0)

# Ponentes

class PonenteTests(APITestCase):
    def setUp(self):
        self.ponente_data = {
            'cedula': '1234567890',
            'nombre': 'Juan',
            'apellido': 'Pérez',
            'correo': 'juan.perez@example.com',
            'telefono': '0987654321',
            'biografia': 'Un ponente muy capacitado.',
            'hora_inicio': '10:00:00',
            'hora_fin': '11:00:00'
        }
        self.ponente = Ponente.objects.create(**self.ponente_data)
        self.url_list_create = reverse('api_ponentes_list_create')
        self.url_detail = reverse('api_ponentes_detail', kwargs={'pk': self.ponente.pk})

    def test_create_ponente(self):
        response = self.client.post(self.url_list_create, self.ponente_data, format='json')
        print(f'\nTest: test_create_ponente\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ponente.objects.count(), 2)

    def test_list_ponentes(self):
        response = self.client.get(self.url_list_create, format='json')
        print(f'\nTest: test_list_ponentes\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_ponente(self):
        response = self.client.get(self.url_detail, format='json')
        print(f'\nTest: test_retrieve_ponente\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], self.ponente.nombre)

    def test_update_ponente(self):
        updated_data = self.ponente_data.copy()
        updated_data['nombre'] = 'Carlos'
        response = self.client.put(self.url_detail, updated_data, format='json')
        print(f'\nTest: test_update_ponente\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ponente.refresh_from_db()
        self.assertEqual(self.ponente.nombre, 'Carlos')

    def test_partial_update_ponente(self):
        response = self.client.patch(self.url_detail, {'nombre': 'Carlos'}, format='json')
        print(f'\nTest: test_partial_update_ponente\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ponente.refresh_from_db()
        self.assertEqual(self.ponente.nombre, 'Carlos')

    def test_delete_ponente(self):
        response = self.client.delete(self.url_detail, format='json')
        print(f'\nTest: test_delete_ponente\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ponente.objects.count(), 0)

# Inscripciones

class InscripcionConcursoTests(APITestCase):
    def setUp(self):
        self.concurso = Concurso.objects.create(
            nombre='Concurso de Programación',
            descripcion='Un concurso para los mejores programadores.',
            fecha_inicio='2023-06-23',
            fecha_fin='2023-06-24',
            competencia_individual=True,
            max_integrantes=1,
            valor_inscripcion=10.0
        )
        self.inscripcion_data = {
            'cedula': '1234567890',
            'nombre': 'Luis',
            'apellido': 'García',
            'telefono': '0987654321',
            'correo': 'luis.garcia@example.com',
            'carrera': 'Ingeniería en Sistemas',
            'semestre': 5,
            'concurso': self.concurso
        }
        self.inscripcion = InscripcionConcurso.objects.create(**self.inscripcion_data)
        self.url_list_create = reverse('api_inscripciones_list_create')
        self.url_detail = reverse('api_inscripciones_detail', kwargs={'pk': self.inscripcion.pk})

    def test_create_inscripcion(self):
        inscripcion_data = {
            'cedula': '9876543210',
            'nombre': 'Carlos',
            'apellido': 'Pérez',
            'telefono': '0987654321',
            'correo': 'carlos.perez@example.com',
            'carrera': 'Ingeniería en Electrónica',
            'semestre': 6,
            'concurso': self.concurso.id
        }
        response = self.client.post(self.url_list_create, inscripcion_data, format='json')
        print(f'\nTest: test_create_inscripcion\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InscripcionConcurso.objects.count(), 2)

    def test_list_inscripciones(self):
        response = self.client.get(self.url_list_create, format='json')
        print(f'\nTest: test_list_inscripciones\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_inscripcion(self):
        response = self.client.get(self.url_detail, format='json')
        print(f'\nTest: test_retrieve_inscripcion\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], self.inscripcion.nombre)

    def test_update_inscripcion(self):
        updated_data = self.inscripcion_data.copy()
        updated_data['nombre'] = 'Carlos'
        updated_data['concurso'] = self.concurso.id
        response = self.client.put(self.url_detail, updated_data, format='json')
        print(f'\nTest: test_update_inscripcion\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.inscripcion.refresh_from_db()
        self.assertEqual(self.inscripcion.nombre, 'Carlos')

    def test_partial_update_inscripcion(self):
        response = self.client.patch(self.url_detail, {'nombre': 'Carlos'}, format='json')
        print(f'\nTest: test_partial_update_inscripcion\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.inscripcion.refresh_from_db()
        self.assertEqual(self.inscripcion.nombre, 'Carlos')

    def test_delete_inscripcion(self):
        response = self.client.delete(self.url_detail, format='json')
        print(f'\nTest: test_delete_inscripcion\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(InscripcionConcurso.objects.count(), 0)
