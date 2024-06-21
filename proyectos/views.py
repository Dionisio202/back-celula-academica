# views.py
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Proyecto
from .serializers import ProyectoSerializer
##Aqui se crea el proyecto , ojo que lso errores ya te los data el serializer por eso no se hace validacion de errores
#POr ejemplo si el usuario no esta activo o no existe  el serializer ya te lo dice
#Si el proyecto ya existe tambien te lo dice el serializer
#Si el proyecto se creo correctamente te regresa el proyecto creado
#Si no se creo correctamente te regresa los errores
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def register_proyecto(request):
    serializer = ProyectoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(creador=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#pk quiere decir la primary key del proyecto
#para poder hacer todos estos metodos teienes que mandarle el token en el header
#de un usuario autenticado y activo 
#Si el proyecto no existe te regresa un error 404
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_proyecto(request, pk):
    proyecto = get_object_or_404(Proyecto, pk=pk)
    if request.user != proyecto.creador:
        return Response({'error': 'No tiene permiso para modificar este proyecto'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = ProyectoSerializer(proyecto, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#Aqui se busca el proyecto por el nombre
#Si no se proporciona un nombre te regresa un error 400
#Si se proporciona un nombre te regresa los proyectos que contienen ese nombre
#como es get tiene que ser un parametro en el link
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def search_proyecto(request):
    nombre = request.query_params.get('nombre', None)
    if nombre:
        proyectos = Proyecto.objects.filter(nombre__icontains=nombre)
        serializer = ProyectoSerializer(proyectos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'error': 'Debe proporcionar un nombre para la búsqueda'}, status=status.HTTP_400_BAD_REQUEST)
#Aqui se elimina el proyecto por el nombre
#Si no se proporciona un nombre te regresa un error 400
#Si se proporciona un nombre te regresa los proyectos que contienen ese nombre
#EL nombre le tienes que poner en body raw de postman
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_proyecto(request):
    try:
        nombre = request.data.get('nombre', None)
        if not nombre:
            return Response({'error': 'Debe proporcionar un nombre para eliminar los proyectos'}, status=status.HTTP_400_BAD_REQUEST)
        proyectos = Proyecto.objects.filter(nombre=nombre, creador=request.user)
        if not proyectos.exists():
            return Response({'error': 'No se encontraron proyectos con ese nombre o no tiene permiso para eliminarlos'}, status=status.HTTP_404_NOT_FOUND)
        
        proyectos.delete()
        return Response({'message': 'Proyectos eliminados correctamente'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
