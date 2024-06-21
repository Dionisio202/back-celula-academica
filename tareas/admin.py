from django.contrib import admin
from django.utils.html import format_html
from .models import Tarea

class TareaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_limite', 'estado', 'mostrar_imagen')  # Agregar 'mostrar_imagen' a los campos a mostrar
    list_filter = ('estado', 'fecha_limite') 
    search_fields = ('nombre',)

    def mostrar_imagen(self, obj):
        if obj.fotografias:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" width="50"  /></a>',
                obj.fotografias.url,
                obj.fotografias.url,
                obj.fotografias.url
            )
        else:
            return '(Sin imagen)'
    mostrar_imagen.short_description = 'Imagen'  

admin.site.register(Tarea, TareaAdmin)
admin.site.site_header = 'Celula Academica'