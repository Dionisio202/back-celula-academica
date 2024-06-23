from django import forms
from .models import Concurso, Charla, Ponente, InscripcionConcurso

class ConcursoForm(forms.ModelForm):
    class Meta:
        model = Concurso
        fields = ['nombre', 'descripcion', 'fecha_inicio', 'fecha_fin', 'competencia_individual', 'max_integrantes', 'valor_inscripcion']

class CharlaForm(forms.ModelForm):
    class Meta:
        model = Charla
        fields = ['nombre', 'imagen','descripcion', 'fecha_inicio', 'fecha_fin', 'ponentes']

class PonenteForm(forms.ModelForm):
    class Meta:
        model = Ponente
        fields = ['cedula', 'nombre', 'apellido', 'correo', 'telefono', 'biografia', 'hora_inicio', 'hora_fin']
class InscripcionConcursoForm(forms.ModelForm):
    class Meta:
        model = InscripcionConcurso
        fields = ['cedula', 'nombre', 'apellido', 'telefono', 'correo', 'carrera', 'semestre', 'nombre_grupo']