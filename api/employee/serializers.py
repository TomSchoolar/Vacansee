from rest_framework import serializers
from .models import Application, Profile

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class SummaryProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['UserId', 'FirstName', 'LastName', 'Pronouns', 'TimeZone', 'PhoneNumber']
