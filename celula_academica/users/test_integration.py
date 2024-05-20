from django.test import TestCase, Client
from django.urls import reverse
from tareas.models import Proyecto, Tarea
from users.models import CustomUser
from datetime import date
from django.contrib.auth.models import Group

class ProyectoTareaIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Crear un grupo de prueba
        self.group = Group.objects.create(name='Coli')
        # Crear un usuario de prueba
        self.usuario_prueba = CustomUser.objects.create_user(
            email='test@example.com',
            nombre='Test',
            apellido='User',
            cedula='123456789',
            telefono='123456789',
            carrera='Test Carrera',
            semestre=1,
            categoria=self.group,  # Utilizamos el objeto de grupo creado anteriormente
            password='password123'
        )
        # Crear datos de prueba para un proyecto
        self.datos_proyecto = {
            'nombre': 'Proyecto de prueba',
            'descripcion': 'Descripción del proyecto de prueba',
            'fecha_inicio': date.today(),
            'fecha_fin': date.today(),
            'creador': self.usuario_prueba.id,  # Enviar el ID del usuario en lugar del objeto
            
        }

    def test_crear_proyecto_y_tarea(self):
        # Crear un proyecto utilizando los datos de prueba
        self.client.force_login(self.usuario_prueba)  # Iniciar sesión como el usuario de prueba
        response_proyecto = self.client.post(reverse("register_proyecto"), self.datos_proyecto, content_type='application/json')
        print(response_proyecto.data)
        self.assertEqual(response_proyecto.status_code, 200)
        # Verificar que el proyecto se haya creado correctamente
        self.assertTrue(Proyecto.objects.filter(nombre='Proyecto de prueba').exists())
