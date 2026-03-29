from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from .models import Tarea, Proyecto
from django.contrib.auth.models import Group
from users.models import CustomUser
from datetime import date

User = get_user_model()

class CrearTareaTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.group = Group.objects.create(name='Empleado')
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
        cls.proyecto = Proyecto.objects.create(
            nombre='Proyecto de Prueba',
            descripcion='Descripción del proyecto de prueba',
            fecha_inicio='2023-01-01',
            fecha_fin='2023-12-31',
            creador=cls.user
        )
        cls.token = Token.objects.create(user=cls.user)
        cls.url = reverse('crear_tarea')

    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_crear_tarea_con_datos_completos(self):
        valid_data = {
            'nombre': 'Tarea de Prueba',
            'descripcion': 'Descripción de la tarea de prueba',
            'fecha_limite': '2023-12-19',
            'estado': 'en_proceso',
            'miembros_responsables': [self.user.id],
            'proyecto': self.proyecto.id
        }
        response = self.client.post(self.url, valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tarea.objects.count(), 1)
        self.assertEqual(Tarea.objects.get().nombre, 'Tarea de Prueba')

    def test_crear_tarea_con_datos_incompletos(self):
        incomplete_data = {
            'nombre': 'Tarea Incompleta',
            'descripcion': 'Descripción de la tarea incompleta',
        }
        response = self.client.post(self.url, incomplete_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Tarea.objects.count(), 0)


class ActualizarTareaTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.group = Group.objects.create(name='Empleado')
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
        cls.proyecto = Proyecto.objects.create(
            nombre='Proyecto de Prueba',
            descripcion='Descripción del proyecto de prueba',
            fecha_inicio='2023-01-01',
            fecha_fin='2023-12-31',
            creador=cls.user
        )
        cls.tarea = Tarea.objects.create(
            nombre='Tarea Inicial',
            descripcion='Descripción inicial de la tarea',
            fecha_limite='2023-12-19',
            estado='sin_asignar',
            proyecto=cls.proyecto
        )
        cls.tarea.miembros_responsables.add(cls.user)
        cls.token = Token.objects.create(user=cls.user)
        cls.url = reverse('actualizar_tarea', kwargs={'pk': cls.tarea.pk})

    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_actualizar_tarea_con_datos_completos(self):
        updated_data = {
            'nombre': 'Tarea Actualizada',
            'descripcion': 'Descripción actualizada de la tarea',
            'fecha_limite': '2023-12-31',
            'estado': 'en_proceso',
            'miembros_responsables': [self.user.id]
        }
        response = self.client.put(self.url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tarea.refresh_from_db()
        self.assertEqual(self.tarea.nombre, 'Tarea Actualizada')
        self.assertEqual(self.tarea.descripcion, 'Descripción actualizada de la tarea')
        self.assertEqual(self.tarea.fecha_limite, date(2023, 12, 31))
        self.assertEqual(self.tarea.estado, 'en_proceso')

    def test_actualizar_tarea_con_datos_incompletos(self):
        incomplete_data = {
            'nombre': ''
        }
        response = self.client.put(self.url, incomplete_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class EliminarTareaTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.group = Group.objects.create(name='Empleado')
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
        cls.proyecto = Proyecto.objects.create(
            nombre='Proyecto de Prueba',
            descripcion='Descripción del proyecto de prueba',
            fecha_inicio='2023-01-01',
            fecha_fin='2023-12-31',
            creador=cls.user
        )
        cls.tarea = Tarea.objects.create(
            nombre='Tarea de Prueba',
            descripcion='Descripción de la tarea de prueba',
            fecha_limite='2023-06-30',
            estado='sin_asignar',
            proyecto=cls.proyecto  
        )
        cls.url = reverse('eliminar_tarea', kwargs={'pk': cls.tarea.pk})
        cls.token = Token.objects.create(user=cls.user)
        
    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_eliminar_tarea(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Tarea.objects.filter(pk=self.tarea.pk).exists())