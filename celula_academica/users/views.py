from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import CustomUser
from rest_framework.authtoken.models import Token
from rest_framework import status 
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes , authentication_classes
from rest_framework.authentication import TokenAuthentication
@api_view(['POST'])
def register(request):
    required_fields = ['email', 'nombre', 'apellido', 'cedula', 'telefono', 'carrera', 'semestre', 'categoria', 'password']
    for field in required_fields:
        if field not in request.data or not request.data[field]:
            return Response({'error': f'El campo "{field}" es requerido'}, status=status.HTTP_400_BAD_REQUEST)
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        nombre = serializer.validated_data['nombre']
        apellido = serializer.validated_data['apellido']
        cedula = serializer.validated_data['cedula']
        telefono = serializer.validated_data['telefono']
        carrera = serializer.validated_data['carrera']
        semestre = serializer.validated_data['semestre']
        categoria = serializer.validated_data['categoria']
        password = serializer.validated_data['password']
        if CustomUser.objects.filter(email=email).exists():
            return Response({'error': 'Este correo electrónico ya está registrado'}, status=status.HTTP_400_BAD_REQUEST)
        if CustomUser.objects.filter(cedula=cedula).exists():
            return Response({'error': 'Esta cedula ya esta registrada'}, status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser.objects.create_user(
            email=email,
            cedula=cedula,
            telefono=telefono,
            carrera=carrera,
            semestre=semestre,
            categoria=categoria,
            password=password,
            nombre=nombre,
            apellido=apellido
        )
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'email': email}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    user=get_object_or_404(CustomUser,email=request.data['email'])
    if not user.check_password(request.data['password']):
        return Response({'error':'Credenciales inválidas'},status=status.HTTP_400_BAD_REQUEST)
    token, created = Token.objects.get_or_create(user=user)
    serializer=UserSerializer(instance=user)
    return Response({'token':token.key,'user':serializer.data},status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    serializer=UserSerializer(instance=request.user)
    return Response(serializer.data,status=status.HTTP_200_OK)