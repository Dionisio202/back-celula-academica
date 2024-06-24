from django.test import TestCase, Client
from rest_framework import status
from .models import Concurso, Charla, Ponente, InscripcionConcurso
from users.models import CustomUser
from django.contrib.auth.models import Group
from django.test import tag
from django.urls import reverse

class IntegrationTest(TestCase):

    def setUp(self):
        self.client = Client()
        
        # Create a group for the user's category
        self.category_group = Group.objects.create(name='Student')

        # Create a user and log in
        self.user = CustomUser.objects.create_user(
            email='user@example.com',
            nombre='Test',
            apellido='User',
            cedula='1234567890',
            telefono='0987654321',
            carrera='Ingeniería',
            semestre=5,
            categoria=self.category_group,
            password='testpassword'
        )
        self.client.login(username='user@example.com', password='testpassword')

        self.concurso_data = {
            'nombre': 'Concurso Test',
            'descripcion': 'Descripción del Concurso Test',
            'fecha_inicio': '2024-06-25',
            'fecha_fin': '2024-06-26',
            'competencia_individual': True,
            'max_integrantes': 5,
            'valor_inscripcion': '10.00'
        }
        self.charla_data = {
            'nombre': 'Charla Test',
            'descripcion': 'Descripción de la Charla Test',
            'fecha_inicio': '2024-06-25',
            'fecha_fin': '2024-06-25',
            'ponentes': []  # Este campo se actualizará más adelante
        }
        self.ponente_data = {
            'cedula': '1234567890',
            'nombre': 'Test',
            'apellido': 'Ponente',
            'correo': 'ponente@example.com',
            'telefono': '1234567890',
            'biografia': 'Biografía del Ponente Test'
        }
        self.inscripcion_data = {
            'cedula': '1234567890',
            'nombre': 'Test',
            'apellido': 'Usuario',
            'telefono': '1234567890',
            'correo': 'test@example.com',
            'carrera': 'Ingeniería',
            'semestre': 5,
        }
        
        # Create a ponente and add it to charla_data
        self.ponente = Ponente.objects.create(**self.ponente_data)
        self.charla_data['ponentes'].append(self.ponente.id)

    @tag('integration')
    def test_create_concurso(self):
        response = self.client.post(reverse('api_concursos_list_create'), self.concurso_data, content_type='application/json')
        print(f'\nTest: test_create_concurso\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nombre'], self.concurso_data['nombre'])

    @tag('integration')
    def test_create_charla(self):
        response = self.client.post(reverse('api_charlas_list_create'), self.charla_data, content_type='application/json')
        print(f'\nTest: test_create_charla\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        if response.status_code != status.HTTP_201_CREATED:
            print(response.content)  # Imprimir el contenido de la respuesta para más detalles
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nombre'], self.charla_data['nombre'])

    @tag('integration')
    def test_create_ponente(self):
        response = self.client.post(reverse('api_ponentes_list_create'), self.ponente_data, content_type='application/json')
        print(f'\nTest: test_create_ponente\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['cedula'], self.ponente_data['cedula'])

    @tag('integration')
    def test_inscripcion_concurso(self):
        concurso = Concurso.objects.create(**self.concurso_data)
        self.inscripcion_data['concurso'] = concurso.id
        response = self.client.post(reverse('api_inscripciones_list_create'), self.inscripcion_data, content_type='application/json')
        print(f'\nTest: test_inscripcion_concurso\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nombre'], self.inscripcion_data['nombre'])

    @tag('integration')
    def test_get_concursos(self):
        Concurso.objects.create(**self.concurso_data)
        response = self.client.get(reverse('api_concursos_list_create'), format='json')
        print(f'\nTest: test_get_concursos\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nombre'], self.concurso_data['nombre'])

    @tag('integration')
    def test_get_charlas(self):
        charla = Charla.objects.create(
            nombre=self.charla_data['nombre'],
            descripcion=self.charla_data['descripcion'],
            fecha_inicio=self.charla_data['fecha_inicio'],
            fecha_fin=self.charla_data['fecha_fin']
        )
        charla.ponentes.set([self.ponente])
        response = self.client.get(reverse('api_charlas_list_create'), format='json')
        print(f'\nTest: test_get_charlas\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nombre'], self.charla_data['nombre'])

    @tag('integration')
    def test_get_ponentes(self):
        response = self.client.get(reverse('api_ponentes_list_create'), format='json')
        print(f'\nTest: test_get_ponentes\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['cedula'], self.ponente_data['cedula'])

    @tag('integration')
    def test_get_inscripciones(self):
        concurso = Concurso.objects.create(**self.concurso_data)
        self.inscripcion_data['concurso'] = concurso
        InscripcionConcurso.objects.create(**self.inscripcion_data)
        response = self.client.get(reverse('api_inscripciones_list_create'), format='json')
        print(f'\nTest: test_get_inscripciones\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nombre'], self.inscripcion_data['nombre'])
