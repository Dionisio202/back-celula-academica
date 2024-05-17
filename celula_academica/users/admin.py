from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

class UserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ('email', 'cedula', 'telefono', 'carrera', 'semestre', 'categoria','is_staff' ,'is_active', 'is_admin')
    list_filter = ('is_active', 'is_admin', 'categoria')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('nombre', 'apellido', 'cedula', 'telefono', 'carrera', 'semestre', 'categoria')}),
        ('Permisos Principales', {'fields': ('is_active', 'is_staff', 'is_admin')}),
    )
    filter_horizontal = ()
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','nombre', 'apellido', 'cedula', 'telefono', 'carrera', 'semestre', 'categoria'),
        }),
    )
    search_fields = ('email', 'nombre', 'apellido','cedula')
    ordering = ('email',)

admin.site.register(CustomUser, UserAdmin)
