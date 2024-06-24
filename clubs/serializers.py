from rest_framework import serializers
from .models import Club, Proyecto
from users.models import CustomUser

class ClubSerializer(serializers.ModelSerializer):
    responsable = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = Club
        fields = '__all__'

class ProyectoSerializer(serializers.ModelSerializer):
    club = serializers.PrimaryKeyRelatedField(queryset=Club.objects.all())

    class Meta:
        model = Proyecto
        fields = '__all__'