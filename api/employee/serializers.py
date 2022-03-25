from rest_framework import serializers
from .models import Application, Favourite, Profile, Reject


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = '__all__'


class RejectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reject
        fields = '__all__'
        

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class SummaryProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['UserId', 'FirstName', 'LastName', 'Pronouns', 'TimeZone', 'PhoneNumber']

        
class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = '__all__'


class RejectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reject
        fields = '__all__'
