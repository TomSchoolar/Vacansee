from copy import copy
from math import ceil
from json import loads
from xml.dom import ValidationErr
from django.forms import ValidationError
from rest_framework import status
from django.db.models import Count, Q
from authentication.models import User
from ..serializers import VacancySerializer
from rest_framework.response import Response
from ..models import EmployerDetails, Vacancy
from rest_framework.decorators import api_view
from authentication.helpers import jwt as jwtHelper
from employer.helpers import getIndex as indexHelper, getReview



@api_view(['GET', 'POST'])
def getIndex(request):
    jwt = jwtHelper.extractJwt(request)

    if type(jwt) is not dict:
        return jwt

    if request.method == 'POST':
        return postIndex(request, jwt)

    # get query params: sort, count, filter, pageNum, uID
    params = request.query_params

    # destructure params and typecast
    try:
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
                UserId__exact = jwt['id'],
                IsOpen__in = filterParam
            ).count()
    pages = int(ceil(numVacancies / int(params['count'])))


    # deals with a lower number of pages than the current page
    while (pageNum - 1) * count >= numVacancies and pageNum > 1:
        pageNum -= 1

    skip = max(count * (pageNum - 1), 0)
    limit = count * pageNum

    # get vacancies
    if sortByApps:
        # sort by the number of applications referencing vacancy
        vacanciesSet = Vacancy.objects.filter(
                UserId__exact = jwt['id'],
                IsOpen__in = filterParam
            ).annotate(
                applicationCount = Count('application', filter=Q(application__ApplicationStatus__exact='PENDING'))
            ).order_by(
                '-applicationCount'
            )[skip:limit]
    else:
        # sort by regular sort param
        vacanciesSet = Vacancy.objects.filter(
            UserId__exact = jwt['id'],
            IsOpen__in = filterParam
        ).order_by(sortParam)[skip:limit]

    
    vacancySerializer = VacancySerializer(vacanciesSet, many=True)
    vacancies = vacancySerializer.data

    try:
        # get company name
        employerDetails = EmployerDetails.objects.get(UserId__exact = jwt['id'])
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



@api_view(['GET'])
def getIndexStats(request):
    # get query params: sort, count, stats, pageNum 
    jwt = jwtHelper.extractJwt(request)

    if type(jwt) is not dict:
        return jwt

    try:
        stats = indexHelper.getStats(jwt['id'])
    except Exception as e:
        return Response(data={'code': 500, 'message': e.__str__}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   
    return Response({ 'stats': stats })



def postIndex(request, jwt):
    try:
        if request.data is not dict:
            data = dict(request.data)
        else:
            data = request.data

        data['UserId'] = User.objects.get(pk = jwt['id'])

        newVacancy = Vacancy(**data)
        newVacancy.full_clean()
        newVacancy.save()

        return Response({ 'status': 200 }, status=status.HTTP_200_OK)
    except ValidationError as err:
        return Response({ 'status': 400, 'message': str(err) }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as err:
        import traceback
        traceback.print_exc()
        print(f'uh oh: { err }')
        return Response({ 'status': 500, 'message': str(err) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def putIndexCloseVacancy(request, vacancyId):
    jwt = jwtHelper.extractJwt(request)

    if type(jwt) is not dict:
        return jwt

    # check vacancyId is valid for that user
    if (not indexHelper.checkUserOwnsVacancy(vacancyId, jwt)):
        return Response(data={'status': '401', 'message': 'You do not have access to that vacancy.'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        vacancy = Vacancy.objects.get(VacancyId__exact = vacancyId)
        vacancy.IsOpen = False
        vacancy.save()
        return Response(status=status.HTTP_200_OK)
    except ValidationError as err:
        return Response(data={'status': 400, 'message': str(err)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as err:
        print(f'uh oh: { err }')
        return Response(data={'status':500, 'message':'Server error while finding and deleting account'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def deleteIndexDeleteVacancy(request, vacancyId):
    jwt = jwtHelper.extractJwt(request)

    if type(jwt) is not dict:
        return jwt

    # check vacancyId is valid for that user
    if (not indexHelper.checkUserOwnsVacancy(vacancyId, jwt)):
        return Response(data={'status': '401', 'message': 'You do not have access to that vacancy.'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        vacancy = Vacancy.objects.get(VacancyId__exact = vacancyId)
        vacancy.delete()
        return Response(status=status.HTTP_200_OK)

    except Exception as err:
        print(f'uh oh: { err }')
        return Response(data={'status':500, 'message':'Server error while finding and deleting account'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)