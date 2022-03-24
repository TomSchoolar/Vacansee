from django.shortcuts import render
from math import ceil
from rest_framework import status
from rest_framework.response import Response
from employer.models import EmployerDetails, Vacancy
from django.db.models import Count, Q
from rest_framework.decorators import api_view
from employer.serializers import VacancySerializer
from employer.helpers import getIndex as indexHelper


# Create your views here.

@api_view(['GET'])
def getIndex(request):
    # get query params: sort, count, filter, pageNum
    params = request.query_params

    # destructure params and typecast
    try:
        uID = params['uID']
        sort = params['sort']
        filter = params['filter']
        count = int(params['count'])
        pageNum = int(params['pageNum'])
        sortByApps = False
    except:
        return Response(data={'status': 400, 'message': 'incomplete request data'}, status=status.HTTP_400_BAD_REQUEST)

    # parse sort parameter into django sort parameter
    if sort == 'newApps':
        sortByApps = True
    elif sort == 'dateDesc':
        sortParam = '-Created'
    elif sort == 'dateAsc':
        sortParam = 'Created'
    elif sort == 'titleAsc':
        sortParam = 'VacancyName'
    else:
        # 'titleDesc'
        sortParam = '-VacancyName'

    # parse filter parameter into django filter parameter
    if filter == 'closed':
        filterParam = [False]
    elif filter == 'active':
        filterParam = [True]
    else:
        # 'all'
        filterParam = [True, False]

    # get number of pages
    numVacancies = Vacancy.objects.filter(
                #UserId__exact = uID,
                IsOpen__in = filterParam
            ).count()
    pages = int(ceil(numVacancies / int(params['count'])))

    # deals with a lower number of pages than the current page
    while (pageNum - 1) * count >= numVacancies and pageNum > 0:
        pageNum -= 1

    skip = max(count * (pageNum - 1), 0)
    limit = count * pageNum

    # get vacancies
    if sortByApps:
        # sort by the number of applications referencing vacancy
        vacanciesSet = Vacancy.objects.filter(
                #UserId__exact = uID,
                IsOpen__in = filterParam
            ).annotate(
                applicationCount = Count('application', filter=Q(application__ApplicationStatus__exact='PENDING'))
            ).order_by(
                '-applicationCount'
            )[skip:limit]
    else:
        # sort by regular sort param
        vacanciesSet = Vacancy.objects.filter(
            #UserId__exact=4,
            IsOpen__in = filterParam
        ).order_by(sortParam)[skip:limit]

    
    vacancySerializer = VacancySerializer(vacanciesSet, many=True)
    vacancies = vacancySerializer.data

    try:
        # get company name
        employerDetails = EmployerDetails.objects.all()
        companyName = employerDetails.CompanyName

        # get number of new, matched and rejected apps for each vacancy
        indexHelper.getVacancyStats(vacancies)
    except EmployerDetails.DoesNotExist:
        return Response(data={'code': 500, 'message': 'error getting company name or stats'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as err:
        print(f'uh oh: { err }')
        return Response(data={'code': 500, 'message': 'Server error getting company name and stats'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # compile return data and send response
    returnData = {
        'numPages': pages,
        'vacancies': vacancies,
        'companyName': companyName,
        'numVacancies': numVacancies
    }

    return Response(returnData)
