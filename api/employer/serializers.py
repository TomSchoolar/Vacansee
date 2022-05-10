from rest_framework import serializers
from .models import Vacancy, EmployerDetails, Tag

class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = '__all__'

class EmployerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployerDetails
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'