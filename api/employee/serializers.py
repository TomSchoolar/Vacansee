from rest_framework import serializers
from .models import Application, Favourite, Reject


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