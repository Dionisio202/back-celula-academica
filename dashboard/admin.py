# dashboard/admin.py
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

class MyAdminSite(admin.AdminSite):
    site_header = 'Mi Administración'
    site_title = 'Mi Administración'
    index_title = 'Bienvenido a Mi Administración'

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='financial_dashboard'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        from .views import financial_dashboard
        return financial_dashboard(request)

admin_site = MyAdminSite(name='myadmin')
