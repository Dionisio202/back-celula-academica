"""
URL configuration for celula_academica project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path ,include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_url = "https://admin-celula-academica.onrender.com/dashboard/"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),
     path('proyects/', include('proyectos.urls')),
    path('tasks/', include('tareas.urls')),
    path('clubs/', include('clubs.urls')),
    path('eventos/', include('eventos.urls')),
    path('api/eventos/', include('eventos.api_urls')),
    path('finanzas/', include('finanzas.urls')), 
    path('api/finanzas/', include('finanzas.api_urls')),
    path('dashboard/', include('dashboard.urls')),  # Agregar esta línea


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
