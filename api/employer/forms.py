from .models import Vacancy
from django.forms import ModelForm



class VacancyForm(ModelForm):
    class Meta:
        model = Vacancy
        fields = '__all__'