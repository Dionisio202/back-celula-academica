from django.urls import path
from .views import RegistrarPagoInscripcionView, RegistrarIngresoEconomicoView, RegistrarEgresoEconomicoView

urlpatterns = [
    path('registrar_pago_inscripcion/', RegistrarPagoInscripcionView.as_view(), name='registrar_pago_inscripcion'),
    path('registrar_ingreso_economico/', RegistrarIngresoEconomicoView.as_view(), name='registrar_ingreso_economico'),
    path('registrar_egreso_economico/', RegistrarEgresoEconomicoView.as_view(), name='registrar_egreso_economico'),
]
