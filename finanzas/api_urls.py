from django.urls import path
from .api_views import (
    PagoInscripcionListCreateAPIView, PagoInscripcionRetrieveUpdateDestroyAPIView,
    IngresoEconomicoListCreateAPIView, IngresoEconomicoRetrieveUpdateDestroyAPIView,
    EgresoEconomicoListCreateAPIView, EgresoEconomicoRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    # URLs para PagoInscripcion
    path('pagos/', PagoInscripcionListCreateAPIView.as_view(), name='pagoinscripcion-list-create'),
    path('pagos/<int:pk>/', PagoInscripcionRetrieveUpdateDestroyAPIView.as_view(), name='pagoinscripcion-detail'),

    # URLs para IngresoEconomico
    path('ingresos/', IngresoEconomicoListCreateAPIView.as_view(), name='ingresoeconomico-list-create'),
    path('ingresos/<int:pk>/', IngresoEconomicoRetrieveUpdateDestroyAPIView.as_view(), name='ingresoeconomico-detail'),

    # URLs para EgresoEconomico
    path('egresos/', EgresoEconomicoListCreateAPIView.as_view(), name='egresoeconomico-list-create'),
    path('egresos/<int:pk>/', EgresoEconomicoRetrieveUpdateDestroyAPIView.as_view(), name='egresoeconomico-detail'),
]
