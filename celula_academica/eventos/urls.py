from django.urls import path
from .views import CrearCharlaView, CrearConcursoView, CrearPonenteView, InscribirseConcursoView

urlpatterns = [
    path('crear_concurso/', CrearConcursoView.as_view(), name='crear_concurso'),
    path('crear_charla/', CrearCharlaView.as_view(), name='crear_charla'),
    path('crear_ponente/', CrearPonenteView.as_view(), name='crear_ponente'),
    path('inscribirse_concurso/<int:concurso_id>/', InscribirseConcursoView.as_view(), name='inscribirse_concurso'),

]
