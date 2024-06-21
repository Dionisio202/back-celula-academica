from django.contrib import admin
from .models import PagoInscripcion, IngresoEconomico, EgresoEconomico

class PagoInscripcionAdmin(admin.ModelAdmin):
    list_display = ('inscripcion', 'fecha_pago', 'monto')
    search_fields = ('inscripcion__nombre', 'inscripcion__apellido')

class IngresoEconomicoAdmin(admin.ModelAdmin):
    list_display = ('fecha_ingreso', 'monto', 'tipo_ingreso', 'concurso')
    search_fields = ('tipo_ingreso', 'concurso__nombre')

class EgresoEconomicoAdmin(admin.ModelAdmin):
    list_display = ('fecha_egreso', 'monto', 'descripcion', 'tipo_egreso', 'concurso')
    search_fields = ('tipo_egreso', 'concurso__nombre')

admin.site.register(PagoInscripcion, PagoInscripcionAdmin)
admin.site.register(IngresoEconomico, IngresoEconomicoAdmin)
admin.site.register(EgresoEconomico, EgresoEconomicoAdmin)
