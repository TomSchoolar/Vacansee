from .models import Vacancy
from rest_framework import serializers

class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = '__all__'