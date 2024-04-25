from rest_framework.views import APIView
from rest_framework.response import Response
from supabase_py import create_client
import os
from dotenv import load_dotenv
from .models import Profile
load_dotenv()
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')
def get_supabase_client():
    return create_client(supabase_url, supabase_key)

class Register(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            name = request.data.get('name')
            lastName = request.data.get('lastName')
            
            if not email or not password:
                return Response({'error': 'Debes proporcionar un correo electrónico y una contraseña'}, status=400)
            if not name or not lastName:
                return Response({'error': 'Debes proporcionar un nombre y un apellido'}, status=400)
            if Profile.objects.filter(email=email).exists():
                return Response({'error': 'El correo electrónico ya está registrado'}, status=400)
            if password.__len__() < 6:
                return Response({'error': 'La contraseña debe tener al menos 6 caracteres'}, status=400)
            client = get_supabase_client()
            auth_response = client.auth.sign_up(email, password)
        
            if 'status_code' in auth_response and auth_response['status_code'] == 200:
                user_id = auth_response.get('id')
                new_profile = Profile.objects.create(
                    user_id=user_id,
                    name=name,
                    last_name=lastName,
                    email=email
                )
                new_profile.save()
                return Response({'Registrado con éxito'}, status=200)
            elif 'status_code' in auth_response and auth_response['status_code'] == 429:
                return Response({'error': 'Límite de registros excedidos'}, status=429)
            else:

                return Response({'error': 'Error en el registro'}, status=400)
        
        except Exception as e:
            return Response({'error': str(e)}, status=500)




class Login(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            if not email or not password:
                return Response({'error': 'Debes proporcionar un correo electrónico y una contraseña'}, status=400)

            client = get_supabase_client()
            auth_response = client.auth.sign_in(email, password)
            if 'status_code' in auth_response and auth_response['status_code'] == 200:
                return Response({'token': auth_response['access_token']})
            else:
                return Response({'error': 'Credenciales inválidas'}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
