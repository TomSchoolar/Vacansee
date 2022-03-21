import regex as re
import jwt as jwtLib
from math import ceil
from .models import Vacancy
from rest_framework import status
from django.db.models import Count, Q
from .serializers import VacancySerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from employer.helpers import getIndex as indexHelper, getReview as reviewHelper



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

    # get number of new, matched and rejected apps for each vacancy
    indexHelper.getVacancyStats(vacancies)

    # compile return data and send response
    returnData = {
        'vacancies': vacancies,
        'numPages': pages,
        'numVacancies': numVacancies
    }

    return Response(returnData)



@api_view(['GET'])
def getIndexStats(request):
    # get query params: sort, count, stats, pageNum 
    params = request.query_params

    # destructure params and typecast
    uID = params['uID']

    try:
        stats = indexHelper.getStats(uID)
    except Exception as e:
        return Response(data={'code': 500, 'message': e.__str__}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   
    return Response({ 'stats': stats })


@api_view(['GET'])
def getReview(request, vacancyId):
    # get jwt
    
    try:
        jwt = reviewHelper.extractJwt(request)
    except jwtLib.ExpiredSignatureError:
        return Response({ 'status': 401, 'message': 'Expired auth token' }, status=status.HTTP_401_UNAUTHORIZED)
    except (AttributeError, jwtLib.InvalidKeyError, jwtLib.InvalidSignatureError, jwtLib.InvalidTokenError):
        return Response({ 'status': 401, 'message': 'Invalid auth token' }, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as err:
        print(f'uh oh: { err }')
        return Response({ 'status': 500, 'message': 'Error acquiring auth token' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        vacancy = reviewHelper.checkUserOwnsVacancy(vacancyId, jwt)
    except Exception as err:
        print(f'uh oh: { err }')
        return Response({ 'status': 500, 'message': 'Error acquiring auth token' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    if not vacancy:
        return Response({ 'status': 401, 'message': 'You do not have access to that vacancy' }, status=status.HTTP_401_UNAUTHORIZED)

    try:
        applications = reviewHelper.getApplications(vacancyId)
    except Exception as err:
        print(f'uh oh: { err }')
        return Response({ 'status': 500, 'message': 'Error getting applications' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    return Response(applications)