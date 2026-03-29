from rest_framework import generics, status
from rest_framework.response import Response
from .models import Concurso, Charla, Ponente, InscripcionConcurso
from .serializers import ConcursoSerializer, CharlaSerializer, PonenteSerializer, InscripcionConcursoSerializer

class ConcursoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Concurso.objects.all()
    serializer_class = ConcursoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ConcursoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Concurso.objects.all()
    serializer_class = ConcursoSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class CharlaListCreateAPIView(generics.ListCreateAPIView):
    queryset = Charla.objects.all()
    serializer_class = CharlaSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class CharlaRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Charla.objects.all()
    serializer_class = CharlaSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class PonenteListCreateAPIView(generics.ListCreateAPIView):
    queryset = Ponente.objects.all()
    serializer_class = PonenteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class PonenteRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ponente.objects.all()
    serializer_class = PonenteSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class InscripcionConcursoListCreateAPIView(generics.ListCreateAPIView):
    queryset = InscripcionConcurso.objects.all()
    serializer_class = InscripcionConcursoSerializer

    def perform_create(self, serializer):
        concurso = serializer.validated_data.get('concurso')
        nombre_grupo = serializer.validated_data.get('nombre_grupo')

        if concurso.max_integrantes is not None:
            if not nombre_grupo or any(char.isdigit() for char in nombre_grupo):
                error_message = 'El nombre de grupo no puede contener números ni estar en blanco'
                return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)
            else:
                integrantes_actuales = concurso.inscripciones.filter(nombre_grupo=nombre_grupo).count()
                if integrantes_actuales >= concurso.max_integrantes:
                    error_message = 'Se ha alcanzado el número máximo de integrantes para ese nombre de grupo.'
                    return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)
        elif nombre_grupo:
            error_message = 'No puede ingresar un nombre de grupo si el concurso no permite grupos.'
            return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)

        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.perform_create(serializer)
        if isinstance(response, Response):
            return response
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
class InscripcionConcursoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InscripcionConcurso.objects.all()
    serializer_class = InscripcionConcursoSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
