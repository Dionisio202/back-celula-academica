from rest_framework import serializers
from .models import PagoInscripcion, IngresoEconomico, EgresoEconomico

class PagoInscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagoInscripcion
        fields = '__all__'

class IngresoEconomicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngresoEconomico
        fields = '__all__'

class EgresoEconomicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EgresoEconomico
        fields = '__all__'