from .models import Application
from .models import Favourite
from rest_framework import serializers

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'

class FavouriteSerializer(serializers.FavouriteSerializer):
    class Meta:
        model = Favourite
        fields = '__all__'