from rest_framework import serializers
from .models import Concurso, Charla, Ponente, InscripcionConcurso

class ConcursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concurso
        fields = ['id', 'nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'competencia_individual', 'max_integrantes', 'valor_inscripcion']

class CharlaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charla
        fields = ['id', 'nombre', 'imagen', 'descripcion', 'fecha_inicio', 'fecha_fin', 'ponentes']

class PonenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ponente
        fields = ['id', 'cedula', 'nombre', 'apellido', 'correo', 'telefono', 'biografia', 'hora_inicio', 'hora_fin']

class InscripcionConcursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InscripcionConcurso
        fields = ['id', 'cedula', 'nombre', 'apellido', 'telefono', 'correo', 'carrera', 'semestre', 'concurso','nombre_grupo']
