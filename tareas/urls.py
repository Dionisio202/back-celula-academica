from django.urls import path
from . import views

urlpatterns = [
    path('crear_tarea/', views.crear_tarea, name='crear_tarea'),
    path('actualizar_tarea/<int:pk>/', views.actualizar_tarea, name='actualizar_tarea'),
    path('eliminar_tarea/<int:pk>/', views.eliminar_tarea, name='eliminar_tarea'),
    path('buscar_tarea/', views.buscar_tarea_por_nombre, name='buscar_tarea_por_nombre'),
]