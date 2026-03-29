from django.test import TestCase, Client
from rest_framework import status
from django.urls import reverse
from .models import PagoInscripcion, IngresoEconomico, EgresoEconomico
from eventos.models import Concurso, InscripcionConcurso
from users.models import CustomUser
from django.contrib.auth.models import Group
from django.test import tag



class EconomicoIntegrationTest(TestCase):

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

        # Create Concurso
        self.concurso = Concurso.objects.create(
            nombre='Concurso Test',
            descripcion='Descripción del Concurso Test',
            fecha_inicio='2024-06-25',
            fecha_fin='2024-06-26',
            competencia_individual=True,
            max_integrantes=5,
            valor_inscripcion='10.00'
        )

        # Create InscripcionConcurso
        self.inscripcion_concurso = InscripcionConcurso.objects.create(
            cedula='1234567890',
            nombre='Test',
            apellido='Usuario',
            telefono='1234567890',
            correo='test@example.com',
            carrera='Ingeniería',
            semestre=5,
            concurso=self.concurso
        )

        # Define data
        self.pago_data = {
            'inscripcion': self.inscripcion_concurso,
            'fecha_pago': '2024-06-27',
            'monto': '10.00'
        }

        self.ingreso_data = {
            'fecha_ingreso': '2024-06-27',
            'monto': '100.00',
            'tipo_ingreso': 'donacion',
            'concurso': self.concurso
        }

        self.egreso_data = {
            'fecha_egreso': '2024-06-28',
            'monto': '50.00',
            'descripcion': 'Egreso Test',
            'tipo_egreso': 'pagos',
            'concurso': self.concurso
        }

    @tag('integration')
    def test_create_pago_inscripcion(self):
        self.pago_data['inscripcion'] = self.inscripcion_concurso.id  # Use id for API request
        response = self.client.post(reverse('pagoinscripcion-list-create'), self.pago_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['monto'], self.pago_data['monto'])
        print(f"\nTest 'test_create_pago_inscripcion' - Datos de entrada: {self.pago_data}, Datos de salida: {response.data}")

    @tag('integration')
    def test_create_ingreso_economico(self):
        self.ingreso_data['concurso'] = self.concurso.id  # Use id for API request
        response = self.client.post(reverse('ingresoeconomico-list-create'), self.ingreso_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['monto'], self.ingreso_data['monto'])
        print(f"\nTest 'test_create_ingreso_economico' - Datos de entrada: {self.ingreso_data}, Datos de salida: {response.data}")

    @tag('integration')
    def test_create_egreso_economico(self):
        self.egreso_data['concurso'] = self.concurso.id  # Use id for API request
        response = self.client.post(reverse('egresoeconomico-list-create'), self.egreso_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['monto'], self.egreso_data['monto'])
        print(f"\nTest 'test_create_egreso_economico' - Datos de entrada: {self.egreso_data}, Datos de salida: {response.data}")

    @tag('integration')
    def test_get_pago_inscripciones(self):
        PagoInscripcion.objects.create(**self.pago_data)
        response = self.client.get(reverse('pagoinscripcion-list-create'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['monto'], self.pago_data['monto'])
        print(f"\nTest 'test_get_pago_inscripciones' - Datos de entrada: {self.pago_data}, Datos de salida: {response.data}")

    @tag('integration')
    def test_get_ingresos_economicos(self):
        IngresoEconomico.objects.create(**self.ingreso_data)
        response = self.client.get(reverse('ingresoeconomico-list-create'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['monto'], self.ingreso_data['monto'])
        print(f"\nTest 'test_get_ingresos_economicos' - Datos de entrada: {self.ingreso_data}, Datos de salida: {response.data}")

    @tag('integration')
    def test_get_egresos_economicos(self):
        EgresoEconomico.objects.create(**self.egreso_data)
        response = self.client.get(reverse('egresoeconomico-list-create'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['monto'], self.egreso_data['monto'])
        print(f"\nTest 'test_get_egresos_economicos' - Datos de entrada: {self.egreso_data}, Datos de salida: {response.data}")
