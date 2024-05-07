from django.contrib import admin
from .models import Proyecto
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_inicio', 'fecha_fin', 'creador') 
    list_filter = ('fecha_inicio', 'fecha_fin') 
    search_fields = ('nombre',)

admin.site.register(Proyecto, ProyectoAdmin)
