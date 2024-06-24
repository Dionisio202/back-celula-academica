from django.urls import path
from .views import (
    ClubListCreateAPIView, ClubRetrieveUpdateDestroyAPIView,
    ProyectoListCreateAPIView, ProyectoRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    # URLs para Club
    path('api/clubs/', ClubListCreateAPIView.as_view(), name='club-list-create'),
    path('api/clubs/<int:pk>/', ClubRetrieveUpdateDestroyAPIView.as_view(), name='club-detail'),

    # URLs para Proyecto
    path('api/proyectos/', ProyectoListCreateAPIView.as_view(), name='proyecto-list-create'),
    path('api/proyectos/<int:pk>/', ProyectoRetrieveUpdateDestroyAPIView.as_view(), name='proyecto-detail'),
]