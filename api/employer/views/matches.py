from ..models import Vacancy
from rest_framework import status
from django.db.models import Count, Q
from employee.models import Application
from rest_framework.response import Response
from rest_framework.decorators import api_view
from authentication.helpers import jwt as jwtHelper
from employer.helpers import getReview as reviewHelper, getMatch as matchHelper



@api_view(['GET'])
def getMatchVacancies(request):

    jwt = jwtHelper.extractJwt(request)

    if type(jwt) is not dict:
        return jwt

    params = request.query_params

    try:
        sort = params['sort']
        searchValue = params['searchValue']
    except:
        return Response(data={'code': 400, 'message': 'incomplete request data'}, status=status.HTTP_400_BAD_REQUEST)


    if sort == 'matchesDesc':
        sortParam = '-MatchesCount'
    elif sort == 'dateDesc':
        sortParam = '-Created'
    elif sort == 'dateAsc':
        sortParam = 'Created'
    elif sort == 'titleAsc':
        sortParam = 'VacancyName'
    else:
        sortParam = '-VacancyName'

    numVacancies = Vacancy.objects.filter(
        UserId__exact = jwt['id'],
        VacancyName__contains = searchValue
    ).count()

    vacancies = Vacancy.objects.filter(
        UserId__exact = jwt['id'],
        VacancyName__contains = searchValue
    ).annotate(
        MatchesCount = Count('application', filter = Q(
            application__ApplicationStatus__exact='MATCHED',
            application__VacancyId__UserId__exact = jwt['id']
        ))
    ).order_by(sortParam).values()

    returnData = {
        'vacancies': vacancies,
        'numVacancies': numVacancies
    }

    return Response(returnData)



@api_view(['GET'])
def getMatches(request):

    jwt = jwtHelper.extractJwt(request)

    if type(jwt) is not dict:
        return jwt

    params = request.query_params

    try:
        vID = params['vID']
        sort = params['sort']
        searchValue = params['searchValue']
    except:
        return Response(data={'code': 400, 'message': 'incomplete request data'}, status=status.HTTP_400_BAD_REQUEST)

    # add sorting

    matches = reviewHelper.getApplications(vID, sort, searchValue)

    returnData = {
        'matches': matches['matches'],
        'numMatches': matches['totalCount']
    }

    return Response(returnData)



@api_view(['GET'])
def getCard(request):

    jwt = jwtHelper.extractJwt(request)

    if type(jwt) is not dict:
        return jwt

    try:
        params = request.query_params
        applicantId = params['applicantId']
    except:
        return Response(data={'code': 400, 'message': 'incomplete request data'}, status=status.HTTP_400_BAD_REQUEST)

    # add sorting

    details = matchHelper.getDetails(applicantId)

    returnData = {
        'details': details
    }

    return Response(returnData)