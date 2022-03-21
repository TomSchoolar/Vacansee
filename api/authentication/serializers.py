from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['Email']