from django.urls import path
from .api_views import (
    ConcursoListCreateAPIView, ConcursoRetrieveUpdateDestroyAPIView,
    CharlaListCreateAPIView, CharlaRetrieveUpdateDestroyAPIView,
    PonenteListCreateAPIView, PonenteRetrieveUpdateDestroyAPIView,
    InscripcionConcursoListCreateAPIView, InscripcionConcursoRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    path('concursos/', ConcursoListCreateAPIView.as_view(), name='api_concursos_list_create'),
    path('concursos/<int:pk>/', ConcursoRetrieveUpdateDestroyAPIView.as_view(), name='api_concursos_detail'),
    path('charlas/', CharlaListCreateAPIView.as_view(), name='api_charlas_list_create'),
    path('charlas/<int:pk>/', CharlaRetrieveUpdateDestroyAPIView.as_view(), name='api_charlas_detail'),
    path('ponentes/', PonenteListCreateAPIView.as_view(), name='api_ponentes_list_create'),
    path('ponentes/<int:pk>/', PonenteRetrieveUpdateDestroyAPIView.as_view(), name='api_ponentes_detail'),
    path('inscripciones/', InscripcionConcursoListCreateAPIView.as_view(), name='api_inscripciones_list_create'),
    path('inscripciones/<int:pk>/', InscripcionConcursoRetrieveUpdateDestroyAPIView.as_view(), name='api_inscripciones_detail'),
]
