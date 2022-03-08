from .models import Vacancy
from .serializers import VacancySerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def getEmployerIndex(request):
    vacancies = Vacancy.objects.filter(UserId__exact=4)
    serializer = VacancySerializer(vacancies, many=True)
    return Response(serializer.data)