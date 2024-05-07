from django.contrib import admin
from django.utils.html import format_html
from .models import Tarea

class TareaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_limite', 'estado', 'mostrar_imagen')  # Agregar 'mostrar_imagen' a los campos a mostrar
    list_filter = ('estado', 'fecha_limite') 
    search_fields = ('nombre',)

    def mostrar_imagen(self, obj):
        if obj.fotografias:  # Verificar si hay una imagen asociada a la tarea
            return format_html('<img src="{}" width="50" />', obj.fotografias.url)  # Devolver la etiqueta HTML con la URL de la imagen
        else:
            return '(Sin imagen)'  # Si no hay imagen, mostrar un texto indicando que no hay imagen

    mostrar_imagen.short_description = 'Imagen'  # Nombre que se mostrará en la columna del administrador

admin.site.register(Tarea, TareaAdmin)
admin.site.site_header = 'Celula Academica'