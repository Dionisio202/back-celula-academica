from django.shortcuts import render

# Create your views here.
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