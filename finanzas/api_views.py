from rest_framework import generics
from .models import PagoInscripcion, IngresoEconomico, EgresoEconomico
from .serializers import PagoInscripcionSerializer, IngresoEconomicoSerializer, EgresoEconomicoSerializer

# CRUD para PagoInscripcion
class PagoInscripcionListCreateAPIView(generics.ListCreateAPIView):
    queryset = PagoInscripcion.objects.all()
    serializer_class = PagoInscripcionSerializer

class PagoInscripcionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PagoInscripcion.objects.all()
    serializer_class = PagoInscripcionSerializer

# CRUD para IngresoEconomico
class IngresoEconomicoListCreateAPIView(generics.ListCreateAPIView):
    queryset = IngresoEconomico.objects.all()
    serializer_class = IngresoEconomicoSerializer

class IngresoEconomicoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = IngresoEconomico.objects.all()
    serializer_class = IngresoEconomicoSerializer

# CRUD para EgresoEconomico
class EgresoEconomicoListCreateAPIView(generics.ListCreateAPIView):
    queryset = EgresoEconomico.objects.all()
    serializer_class = EgresoEconomicoSerializer

class EgresoEconomicoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EgresoEconomico.objects.all()
    serializer_class = EgresoEconomicoSerializer