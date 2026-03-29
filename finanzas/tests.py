from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from .models import PagoInscripcion, IngresoEconomico, EgresoEconomico, Concurso, InscripcionConcurso
from decimal import Decimal
from datetime import date
from django.contrib.auth.models import Group

CustomUser = get_user_model()

class PagoInscripcionAPITests(APITestCase):
    def setUp(self):
        group = Group.objects.create(name='Test Group')
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            nombre='Nombre',
            apellido='Apellido',
            cedula='1234567890',
            telefono='0987654321',
            carrera='Ingeniería en Sistemas',
            semestre=5,
            categoria=group,
            password='testpassword'
        )
        self.client = APIClient()
        self.client.login(email='testuser@example.com', password='testpassword')
        self.concurso = Concurso.objects.create(
            nombre='Concurso de Programación',
            descripcion='Un concurso para los mejores programadores.',
            fecha_inicio='2024-07-01',
            fecha_fin='2024-07-05',
            competencia_individual=True,
            valor_inscripcion=Decimal('100.00')
        )
        self.inscripcion = InscripcionConcurso.objects.create(
            cedula='1234567890',
            nombre='Luis',
            apellido='García',
            telefono='0987654321',
            correo='luis.garcia@example.com',
            carrera='Ingeniería en Sistemas',
            semestre=5,
            concurso=self.concurso
        )
        self.url = reverse('pagoinscripcion-list-create')

    def test_create_pago_inscripcion(self):
        data = {
            'inscripcion': self.inscripcion.id,
            'fecha_pago': date.today(),
            'monto': '100.00'
        }
        response = self.client.post(self.url, data, format='json')
        print(f'\nTest: test_create_pago_inscripcion\nResponse Data: {response.data} \nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PagoInscripcion.objects.count(), 1)
        self.assertEqual(IngresoEconomico.objects.count(), 1)
        pago = PagoInscripcion.objects.first()
        self.assertEqual(pago.monto, Decimal('100.00'))
        ingreso = IngresoEconomico.objects.first()
        self.assertEqual(ingreso.monto, Decimal('100.00'))

    def test_list_pago_inscripcion(self):
        PagoInscripcion.objects.create(
            inscripcion=self.inscripcion,
            fecha_pago=date.today(),
            monto=Decimal('100.00')
        )
        response = self.client.get(self.url)
        print(f'\nTest: test_list_pago_inscripcion\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_pago_inscripcion(self):
        pago = PagoInscripcion.objects.create(
            inscripcion=self.inscripcion,
            fecha_pago=date.today(),
            monto=Decimal('100.00')
        )
        url = reverse('pagoinscripcion-detail', kwargs={'pk': pago.id})
        response = self.client.get(url)
        print(f'\nTest: test_retrieve_pago_inscripcion\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['monto'], '100.00')

    def test_update_pago_inscripcion(self):
        pago = PagoInscripcion.objects.create(
            inscripcion=self.inscripcion,
            fecha_pago=date.today(),
            monto=Decimal('100.00')
        )
        url = reverse('pagoinscripcion-detail', kwargs={'pk': pago.id})
        data = {
            'inscripcion': self.inscripcion.id,
            'fecha_pago': date.today(),
            'monto': '150.00'
        }
        response = self.client.put(url, data, format='json')
        print(f'\nTest: test_update_pago_inscripcion\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pago.refresh_from_db()
        self.assertEqual(pago.monto, Decimal('150.00'))

    def test_delete_pago_inscripcion(self):
        pago = PagoInscripcion.objects.create(
            inscripcion=self.inscripcion,
            fecha_pago=date.today(),
            monto=Decimal('100.00')
        )
        url = reverse('pagoinscripcion-detail', kwargs={'pk': pago.id})
        response = self.client.delete(url)

        print(f'\nTest: test_delete_pago_inscripcion\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PagoInscripcion.objects.count(), 0)


class IngresoEconomicoAPITests(APITestCase):
    def setUp(self):
        group = Group.objects.create(name='Test Group')
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            nombre='Nombre',
            apellido='Apellido',
            cedula='1234567890',
            telefono='0987654321',
            carrera='Ingeniería en Sistemas',
            semestre=5,
            categoria=group,
            password='testpassword'
        )
        self.client = APIClient()
        self.client.login(email='testuser@example.com', password='testpassword')
        self.url = reverse('ingresoeconomico-list-create')

    def test_create_ingreso_economico(self):
        data = {
            'fecha_ingreso': date.today(),
            'monto': '200.00',
            'tipo_ingreso': 'donacion'
        }
        response = self.client.post(self.url, data, format='json')
        print(f'\nTest: test_create_ingreso_economico\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(IngresoEconomico.objects.count(), 1)
        ingreso = IngresoEconomico.objects.first()
        self.assertEqual(ingreso.monto, Decimal('200.00'))

    def test_list_ingreso_economico(self):
        IngresoEconomico.objects.create(
            fecha_ingreso=date.today(),
            monto=Decimal('200.00'),
            tipo_ingreso='donacion'
        )
        response = self.client.get(self.url)
        print(f'\nTest: test_list_ingreso_economico\nResponse Data: {response.data} \nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_ingreso_economico(self):
        ingreso = IngresoEconomico.objects.create(
            fecha_ingreso=date.today(),
            monto=Decimal('200.00'),
            tipo_ingreso='donacion'
        )
        url = reverse('ingresoeconomico-detail', kwargs={'pk': ingreso.id})
        response = self.client.get(url)
        print(f'\nTest: test_retrieve_ingreso_economico\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['monto'], '200.00')

    def test_update_ingreso_economico(self):
        ingreso = IngresoEconomico.objects.create(
            fecha_ingreso=date.today(),
            monto=Decimal('200.00'),
            tipo_ingreso='donacion'
        )
        url = reverse('ingresoeconomico-detail', kwargs={'pk': ingreso.id})
        data = {
            'fecha_ingreso': date.today(),
            'monto': '250.00',
            'tipo_ingreso': 'concurso'
        }
        response = self.client.put(url, data, format='json')
        print(f'\nTest: test_update_ingreso_economico\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ingreso.refresh_from_db()
        self.assertEqual(ingreso.monto, Decimal('250.00'))

    def test_delete_ingreso_economico(self):
        ingreso = IngresoEconomico.objects.create(
            fecha_ingreso=date.today(),
            monto=Decimal('200.00'),
            tipo_ingreso='donacion'
        )
        url = reverse('ingresoeconomico-detail', kwargs={'pk': ingreso.id})
        response = self.client.delete(url)
        print(f'\nTest: test_delete_ingreso_economico\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(IngresoEconomico.objects.count(), 0)


class EgresoEconomicoAPITests(APITestCase):
    def setUp(self):
        group = Group.objects.create(name='Test Group')
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            nombre='Nombre',
            apellido='Apellido',
            cedula='1234567890',
            telefono='0987654321',
            carrera='Ingeniería en Sistemas',
            semestre=5,
            categoria=group,
            password='testpassword'
        )
        self.client = APIClient()
        self.client.login(email='testuser@example.com', password='testpassword')
        self.url = reverse('egresoeconomico-list-create')

    def test_create_egreso_economico(self):
        data = {
            'fecha_egreso': date.today(),
            'monto': '150.00',
            'descripcion': 'Compra de materiales',
            'tipo_egreso': 'pagos'
        }
        response = self.client.post(self.url, data, format='json')
        print(f'\nTest: test_create_egreso_economico\nResponse Data: {response.data}\nResponse Code: {response.status_code}')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EgresoEconomico.objects.count(), 1)
        egreso = EgresoEconomico.objects.first()
        self.assertEqual(egreso.monto, Decimal('150.00'))

    def test_list_egreso_economico(self):
        EgresoEconomico.objects.create(
            fecha_egreso=date.today(),
            monto=Decimal('150.00'),
            descripcion='Compra de materiales',
            tipo_egreso='pagos'
        )
        response = self.client.get(self.url)
        print(f'\nTest: test_list_egreso_economico\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_egreso_economico(self):
        egreso = EgresoEconomico.objects.create(
            fecha_egreso=date.today(),
            monto=Decimal('150.00'),
            descripcion='Compra de materiales',
            tipo_egreso='pagos'
        )
        url = reverse('egresoeconomico-detail', kwargs={'pk': egreso.id})
        response = self.client.get(url)
        print(f'\nTest: test_retrieve_egreso_economico\nResponse Data: {response.data}\nResponse Code: {response.status_code}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['monto'], '150.00')

    def test_update_egreso_economico(self):
        egreso = EgresoEconomico.objects.create(
            fecha_egreso=date.today(),
            monto=Decimal('150.00'),
            descripcion='Compra de materiales',
            tipo_egreso='pagos'
        )
        url = reverse('egresoeconomico-detail', kwargs={'pk': egreso.id})
        data = {
            'fecha_egreso': date.today(),
            'monto': '180.00',
            'descripcion': 'Compra de servicios',
            'tipo_egreso': 'concurso'
        }
        response = self.client.put(url, data, format='json')
        print(f'\nTest: test_update_egreso_economico\nResponse Data: {response.data}\nResponse Code: {response.status_code}')
       
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        egreso.refresh_from_db()
        self.assertEqual(egreso.monto, Decimal('180.00'))

    def test_delete_egreso_economico(self):
        egreso = EgresoEconomico.objects.create(
            fecha_egreso=date.today(),
            monto=Decimal('150.00'),
            descripcion='Compra de materiales',
            tipo_egreso='pagos'
        )
        url = reverse('egresoeconomico-detail', kwargs={'pk': egreso.id})
        response = self.client.delete(url)
        print(f'\nTest: test_delete_egreso_economico\nResponse Data: {response.data}\nResponse Code: {response.status_code}')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(EgresoEconomico.objects.count(), 0)
