from .models import RefreshToken, User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RefreshTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefreshToken
        fields = '__all__'