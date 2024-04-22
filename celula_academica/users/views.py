from rest_framework.views import APIView
from rest_framework.response import Response
from supabase_py import create_client

class Register(APIView):
    def post(self, request):
        # Obtener datos de la solicitud
     try:
        email = request.query_params.get('email')
        password = request.query_params.get('password')
        name=request.query_params.get('name')
        lastName=request.query_params.get('lastName')
        if not email or not password:
            return Response({'error': 'Debes proporcionar un correo electrónico y una contraseña'}, status=400)

        # Configurar el cliente Supabase
        supabase_url = 'https://esdqjitrbfjfnpkmizyx.supabase.co'
        supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVzZHFqaXRyYmZqZm5wa21penl4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTMyMjEwODYsImV4cCI6MjAyODc5NzA4Nn0.LxIA5PdtDASqPQHCWPFz8zTzVO83-oEPyTUJp_qUaIs'
        client = create_client(supabase_url, supabase_key)

        auth_response = client.auth.sign_up(email, password)
        
        if 'status_code' in auth_response and auth_response['status_code'] == 200:
            user_id = auth_response.get('id')
            profile_data = {
                    'user_id': user_id,
                    'name': name,
                    'last_name':lastName,
                }
            profile_table = client.table('profile')
            profile_response = profile_table.insert(profile_data).execute()
            # Autenticación exitosa
            return Response({'Registrado con exito':auth_response})
        elif 'status_code' in auth_response and auth_response['status_code'] == 429:
            return Response({'Limite de registros excedidos'}, status=429)
     except Exception as e:
            return Response({'error': str(e)}, status=500)



class Login(APIView):
    def post(self, request):
        try:
     
            email = request.data.get('email')
            password = request.data.get('password')

            if not email or not password:
                return Response({'error': 'Debes proporcionar un correo electrónico y una contraseña'}, status=400)

            supabase_url = 'https://esdqjitrbfjfnpkmizyx.supabase.co'
            supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVzZHFqaXRyYmZqZm5wa21penl4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTMyMjEwODYsImV4cCI6MjAyODc5NzA4Nn0.LxIA5PdtDASqPQHCWPFz8zTzVO83-oEPyTUJp_qUaIs'
            client = create_client(supabase_url, supabase_key)

  
            auth_response = client.auth.sign_in(email, password)
          
        
            if 'status_code' in auth_response and auth_response['status_code'] == 200:
                # Autenticación exitosa
                  return Response({'token': auth_response['access_token']})
            else:
                return Response({'error': auth_response.get('error', auth_response)}, status=400)
        except Exception as e:
            return Response({'error': auth_response}, status=500)