from django import forms
from .models import PagoInscripcion, IngresoEconomico, EgresoEconomico

class PagoInscripcionForm(forms.ModelForm):
    class Meta:
        model = PagoInscripcion
        fields = ['inscripcion', 'fecha_pago', 'monto']

class IngresoEconomicoForm(forms.ModelForm):
    class Meta:
        model = IngresoEconomico
        fields = ['fecha_ingreso', 'monto', 'tipo_ingreso', 'concurso']

class EgresoEconomicoForm(forms.ModelForm):
    class Meta:
        model = EgresoEconomico
        fields = ['fecha_egreso', 'monto', 'descripcion', 'tipo_egreso', 'concurso']
