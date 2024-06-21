from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from .models import CustomUser
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

def send_reset_password_email(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    password_reset_url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
    password_reset_link = f"{settings.DOMAIN_NAME}{password_reset_url}"
    
    # Enviar correo electrónico con el enlace de restablecimiento de contraseña
    send_mail(
        'Registro exitoso',
        f'Hola {user.nombre} {user.apellido},\n\nGracias por registrarte. Por favor, haz clic en el siguiente enlace para establecer tu contraseña:\n\n{password_reset_link}',
        settings.EMAIL_HOST_USER,  # Remitente
        [user.email],  # Destinatario (correo del usuario registrado)
        fail_silently=False,
    )

#Registro de usuario
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

        # Validación de datos repetidos
        if CustomUser.objects.filter(email=email).exists():
            return Response({'error': 'Este correo electrónico ya está registrado'}, status=status.HTTP_400_BAD_REQUEST)
        if CustomUser.objects.filter(cedula=cedula).exists():
            return Response({'error': 'Esta cedula ya está registrada'}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.create_user(
            email=email, cedula=cedula, telefono=telefono, carrera=carrera, semestre=semestre, categoria=categoria, password=password, nombre=nombre, apellido=apellido
        )
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'email': email}, status=status.HTTP_201_CREATED)
    
    # Validación de datos en blanco
    if not all(serializer.validated_data.values()):
        return Response({'error': 'No se permiten campos vacíos'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#Login de usuario
@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Credenciales incompletas'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, email=email, password=password)

    #No se puede verificar si las credenciales son correctas porque al bloquearle el usuario 
    #esta en la abse de datos pero es como si no existiera no se puede verificar si las credenciales son correctas    
    if user is None:
        return Response({'error': 'Credenciales incorrectas'}, status=status.HTTP_400_BAD_REQUEST)
   
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_200_OK)
# obtener todo el  Perfil de usuario mediante el token de autenticación
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    serializer = UserSerializer(instance=request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)
#Actualizar usuario
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    serializer = UserSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        email = serializer.validated_data.get('email', user.email)
        cedula = serializer.validated_data.get('cedula', user.cedula)

        if CustomUser.objects.filter(email=email).exclude(pk=user.pk).exists():
            return Response({'error': 'Este correo electrónico ya está registrado'}, status=status.HTTP_400_BAD_REQUEST)
        if CustomUser.objects.filter(cedula=cedula).exclude(pk=user.pk).exists():
            return Response({'error': 'Esta cédula ya está registrada'}, status=status.HTTP_400_BAD_REQUEST)

        # Validación de datos incompletos
        if not all(serializer.validated_data.values()):
            return Response({'error': 'No se permiten campos vacíos'}, status=status.HTTP_400_BAD_REQUEST)

        # Actualiza los datos del usuario
        for key, value in serializer.validated_data.items():
            if key == 'password':
                user.set_password(value)
            else:
                setattr(user, key, value)

        user.save()
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Buscar usuario por nombre o cédula
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def search_user(request):
    nombre = request.query_params.get('nombre', None)
    cedula = request.query_params.get('cedula', None)

    if not nombre and not cedula:
        return Response({'error': 'Debe proporcionar un nombre o una cédula para la búsqueda'}, status=status.HTTP_400_BAD_REQUEST)

    users = CustomUser.objects.all()

    if nombre:
        users = users.filter(nombre__icontains=nombre)

    if cedula:
        users = users.filter(cedula__icontains=cedula)

    if not users.exists():
        return Response({'error': 'No se encontraron usuarios con los criterios de búsqueda'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)