from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from .models import Tarea
from .serializers import TareaSerializer

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def crear_tarea(request):
    serializer = TareaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def actualizar_tarea(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk)
    serializer = TareaSerializer(tarea, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def eliminar_tarea(request, pk):
    tarea = get_object_or_404(Tarea, pk=pk)
    tarea.delete()
    return Response({'message': 'Tarea eliminada correctamente'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def buscar_tarea_por_nombre(request):
    nombre = request.query_params.get('nombre', None)
    if not nombre:
        return Response({'error': 'Debe proporcionar un nombre para buscar la tarea'}, status=status.HTTP_400_BAD_REQUEST)
    tareas = Tarea.objects.filter(nombre__icontains=nombre)
    serializer = TareaSerializer(tareas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
