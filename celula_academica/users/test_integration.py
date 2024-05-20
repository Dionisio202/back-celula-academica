from django.test import TestCase, Client
from django.urls import reverse
from tareas.models import Proyecto, Tarea
from users.models import CustomUser
from datetime import date
from django.contrib.auth.models import Group

class ProyectoTareaIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.group = Group.objects.create(name='Coli')
        self.usuario_prueba = CustomUser.objects.create_user(
            email='test@example.com',
            nombre='Test',
            apellido='User',
            cedula='123456789',
            telefono='123456789',
            carrera='Test Carrera',
            semestre=1,
            categoria=self.group, 
            password='password123'
        )
       
        self.datos_proyecto = {
            'nombre': 'Proyecto de prueba',
            'descripcion': 'Descripción del proyecto de prueba',
            'fecha_inicio': date.today(),
            'fecha_fin': date.today(),
            'creador': self.usuario_prueba.id, 
            
        }

    def test_crear_proyecto_y_tarea(self):
        self.client.force_login(self.usuario_prueba) 
        response_proyecto = self.client.post(reverse("register_proyecto"), self.datos_proyecto, content_type='application/json')
        print(response_proyecto.data)
        self.assertEqual(response_proyecto.status_code, 200)
        self.assertTrue(Proyecto.objects.filter(nombre='Proyecto de prueba').exists())
