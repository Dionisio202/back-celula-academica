from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status 
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes , authentication_classes
from rest_framework.authentication import TokenAuthentication
@api_view(['GET'])
def hello(request):
    return Response({'message':'Hello World!'})