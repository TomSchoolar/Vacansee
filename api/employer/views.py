from .models import Vacancy
from employee.models import Application
from .serializers import VacancySerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from employee.serializers import ApplicationSerializer


@api_view(['GET'])
def getEmployerIndex(request):
    # get vacancies matching userid
    vacanciesSet = Vacancy.objects.filter(UserId__exact=4)
    vacancySerializer = VacancySerializer(vacanciesSet, many=True)
    vacancies = vacancySerializer.data

    # get the number of new, accepted and rejected applications for each vacancy
    for vacancy in vacancies:
        applicationsSet = Application.objects.filter(VacancyId__exact=vacancy['VacancyId'])
        applicationSerializer = ApplicationSerializer(applicationsSet, many=True)
        applications = applicationSerializer.data

        new = 0
        accepted = 0
        rejected = 0
        total = 0

        for application in applications:
            status = application['ApplicationStatus']
            total += 1

            if status == 'PENDING':
                new += 1
            elif status == 'MATCHED':
                accepted += 1
            else:
                rejected += 1
        
        vacancy['NewApplications'] = new
        vacancy['AcceptedApplications'] = accepted
        vacancy['RejectedApplications'] = rejected
        vacancy['Applications'] = total

    return Response(vacancies)
