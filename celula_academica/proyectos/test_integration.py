from django.test import TestCase
from rest_framework.test import APIClient  # Importa el cliente de pruebas de DRF
from django.urls import reverse
from tareas.models import Proyecto, Tarea
from users.models import CustomUser
from datetime import date
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.authtoken.models import Token

class ProyectoTareaIntegrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()  
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
        self.token = Token.objects.create(user=self.usuario_prueba)
        self.client.force_authenticate(user=self.usuario_prueba)  # Autentica al usuario de prueba
        
        self.datos_proyecto = {
            'nombre': 'Proyecto de prueba',
            'descripcion': 'Descripción del proyecto de prueba',
            'fecha_inicio': date.today(),
            'fecha_fin': date.today(),
            'creador': self.usuario_prueba.id,
            'miembros': [self.usuario_prueba.id]
        }

        self.datos_tarea = {
            'nombre': 'Tarea de prueba',
            'descripcion': 'Descripción de la tarea de prueba',
            'fecha_limite': date.today(),
            'estado': 'sin_asignar',
            'miembros_responsables': [self.usuario_prueba.id],
            'proyecto': None 
        }

    def test_crear_proyecto_y_tarea(self):
        response_proyecto = self.client.post(reverse("register_proyecto"), self.datos_proyecto, format='json')
        print(response_proyecto.data)
        self.assertEqual(response_proyecto.status_code, 201)  # Verificar que el proyecto se haya creado correctamente
        self.assertTrue(Proyecto.objects.filter(nombre='Proyecto de prueba').exists())

        proyecto_creado = Proyecto.objects.get(nombre='Proyecto de prueba')
        
        self.datos_tarea['proyecto'] = proyecto_creado.id

        response_tarea = self.client.post(reverse("crear_tarea"), self.datos_tarea, format='json')
        print(response_tarea.data)
        self.assertEqual(response_tarea.status_code, 201)  # Verificar que la tarea se haya creado correctamente
        self.assertTrue(Tarea.objects.filter(nombre='Tarea de prueba', proyecto=proyecto_creado).exists())

    def test_actualizar_proyecto_y_tarea(self):
        proyecto = Proyecto.objects.create(
            nombre="Proyecto original", 
            descripcion="Descripción original", 
            fecha_inicio=date.today(), 
            fecha_fin=date.today(), 
            creador=self.usuario_prueba
        )
        tarea = Tarea.objects.create(
            nombre="Tarea original", 
            descripcion="Descripción original", 
            fecha_limite=date.today(), 
            estado='sin_asignar', 
            proyecto=proyecto
        )

        proyecto_data = {
            "nombre": "Proyecto actualizado", 
            "descripcion": "Descripción actualizada"
        }
        response_proyecto = self.client.put(reverse("update_proyecto", kwargs={"pk": proyecto.id}), proyecto_data, format='json')
        self.assertEqual(response_proyecto.status_code, status.HTTP_200_OK)

        tarea_data = {
            "nombre": "Tarea actualizada", 
            "descripcion": "Descripción actualizada"
        }
        response_tarea = self.client.put(reverse("actualizar_tarea", kwargs={"pk": tarea.id}), tarea_data, format='json')
        self.assertEqual(response_tarea.status_code, status.HTTP_200_OK)

    def test_eliminar_proyecto_y_tarea(self):
        proyecto = Proyecto.objects.create(
            nombre="Proyecto a eliminar", 
            descripcion="Descripción del proyecto a eliminar", 
            fecha_inicio=date.today(), 
            fecha_fin=date.today(), 
            creador=self.usuario_prueba
        )
        tarea = Tarea.objects.create(
            nombre="Tarea a eliminar", 
            descripcion="Descripción de la tarea a eliminar", 
            fecha_limite=date.today(), 
            estado='sin_asignar', 
            proyecto=proyecto
        )

        # Eliminar la tarea
        response_tarea = self.client.delete(reverse("eliminar_tarea", kwargs={"pk": tarea.id}))
        self.assertEqual(response_tarea.status_code, status.HTTP_200_OK)

        # Eliminar el proyecto por su nombre
        nombre_proyecto = "Proyecto a eliminar"
        response_proyecto = self.client.delete(reverse("delete_proyecto"), data={"nombre": nombre_proyecto}, format='json')
        self.assertEqual(response_proyecto.status_code, status.HTTP_200_OK)
