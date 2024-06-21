from django.utils.html import format_html
from django.contrib import admin
from .models import Concurso, Charla, Ponente, InscripcionConcurso

class PonenteAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombre', 'apellido', 'correo', 'telefono', 'hora_inicio', 'hora_fin')
    search_fields = ('nombre', 'apellido', 'cedula')

class ConcursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_inicio', 'fecha_fin', 'competencia_individual', 'max_integrantes', 'valor_inscripcion')
    list_filter = ('fecha_inicio', 'fecha_fin', 'competencia_individual', 'max_integrantes', 'valor_inscripcion')
    search_fields = ('nombre', 'descripcion')

    class Media:
        js = ('eventos/admin.js',)

class CharlaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_inicio', 'fecha_fin', 'mostrar_imagen')
    list_filter = ('fecha_inicio', 'fecha_fin')
    search_fields = ('descripcion', 'nombre')
    filter_horizontal = ('ponentes',)

    def mostrar_imagen(self, obj):
        if obj.imagen:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" width="50" /></a>',
                obj.imagen.url,
                obj.imagen.url,
            )
        else:
            return '(Sin imagen)'
    mostrar_imagen.short_description = 'Imagen'

class InscripcionConcursoAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombre', 'apellido', 'telefono', 'correo', 'carrera', 'semestre', 'fecha_registro', 'concurso')
    search_fields = ('nombre', 'apellido', 'cedula', 'correo')

admin.site.register(Concurso, ConcursoAdmin)
admin.site.register(Charla, CharlaAdmin)
admin.site.register(Ponente, PonenteAdmin)
admin.site.register(InscripcionConcurso, InscripcionConcursoAdmin)
