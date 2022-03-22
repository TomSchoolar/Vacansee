from .models import Application
from .models import Favourite
from .models import Reject
from rest_framework import serializers

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