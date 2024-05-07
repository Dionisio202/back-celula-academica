from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import CustomUser

class UserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ('email', 'cedula', 'telefono', 'carrera', 'semestre', 'categoria', 'is_active', 'is_admin')
    list_filter = ('is_active', 'is_admin', 'categoria')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('nombre', 'apellido', 'telefono', 'cedula', 'carrera', 'semestre', 'categoria')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    filter_horizontal = ('custom_field',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'nombre', 'apellido')
    ordering = ('email',)
    admin.site.register(CustomUser)
