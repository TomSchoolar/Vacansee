from math import ceil
from .models import Vacancy
from django.db.models import Count, Q
from .serializers import VacancySerializer
from rest_framework.response import Response
from .helpers import getIndex as indexHelper
from rest_framework.decorators import api_view



@api_view(['GET'])
def getIndex(request):
    # get query params: sort, count, stats, pageNum 
    params = request.query_params

    # destructure params and typecast
    uID = params['uID']
    sort = params['sort']
    filter = params['filter']
    count = int(params['count'])
    pageNum = int(params['pageNum'])
    stats = bool([1 if x == 'true' else 0 for x in [params['stats']]][0])
    sortByApps = False


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
    if filter == 'all':
        filterParam = [True, False]
    elif filter == 'active':
        filterParam = [True]
    else:
        # 'closed'
        filterParam = [False]


    # get number of pages
    numVacancies = Vacancy.objects.filter(
                UserId__exact = uID,
                IsOpen__in = filterParam
            ).count()
    pages = int(ceil(numVacancies / int(params['count'])))


    # deals with a lower number of pages than the current page
    while (pageNum - 1) * count >= numVacancies and pageNum > 0:
        pageNum -= 1

    skip = count * (pageNum - 1)
    limit = count * pageNum

    # get vacancies
    if sortByApps:
        # sort by the number of applications referencing vacancy
        vacanciesSet = Vacancy.objects.filter(
                UserId__exact = uID,
                IsOpen__in = filterParam
            ).annotate(
                applicationCount = Count('application', filter=Q(application__ApplicationStatus__exact='PENDING'))
            ).order_by(
                '-applicationCount'
            )[skip:limit]
    else:
        # sort by regular sort param
        vacanciesSet = Vacancy.objects.filter(
            UserId__exact=4,
            IsOpen__in = filterParam
        ).order_by(sortParam)[skip:limit]

    
    vacancySerializer = VacancySerializer(vacanciesSet, many=True)
    vacancies = vacancySerializer.data

    if stats:
        statsObj = indexHelper.getStats(uID)
    else:
        statsObj = False

    # get number of new, matched and rejected apps for each vacancy
    indexHelper.getVacancyStats(vacancies)

    # compile return data and send response
    returnData = {
        'vacancies': vacancies,
        'stats': statsObj,
        'numPages': pages,
        'numVacancies': numVacancies
    }

    return Response(returnData)
