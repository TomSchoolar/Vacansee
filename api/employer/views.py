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

    stats = {
        'activeAdverts': 0,
        'totalApplications': 0,
        'newApplications': 0,
        'acceptedApplications': 0,
        'rejectedApplications': 0,
    }

    # get the number of new, accepted and rejected applications for each vacancy
    for vacancy in vacancies:
        applicationsSet = Application.objects.filter(VacancyId__exact=vacancy['VacancyId'])
        applicationSerializer = ApplicationSerializer(applicationsSet, many=True)
        applications = applicationSerializer.data

        if vacancy['IsOpen']:
            stats['activeAdverts'] += 1

        new = 0
        accepted = 0
        rejected = 0
        total = 0

        for application in applications:
            status = application['ApplicationStatus']
            stats['totalApplications'] += 1
            total += 1

            if status == 'PENDING':
                stats['newApplications'] += 1
                new += 1
            elif status == 'MATCHED':
                stats['acceptedApplications'] += 1
                accepted += 1
            else:
                stats['acceptedApplications'] += 1
                rejected += 1
        
        vacancy['NewApplications'] = new
        vacancy['AcceptedApplications'] = accepted
        vacancy['RejectedApplications'] = rejected
        vacancy['Applications'] = total

    returnData = {
        'vacancies': vacancies,
        'stats': stats
    }

    return Response(returnData)
