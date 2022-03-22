import regex as re
import jwt as jwtLib
from math import ceil
from datetime import datetime
from rest_framework import status
from django.db.models import Count, Q
from employee.models import Application
from .serializers import VacancySerializer
from rest_framework.response import Response
from .models import EmployerDetails, Vacancy
from rest_framework.decorators import api_view
from employer.helpers import getIndex as indexHelper, getReview as reviewHelper
from employee.serializers import ApplicationSerializer, SummaryProfileSerializer



@api_view(['GET'])
def getIndex(request):
    # get query params: sort, count, filter, pageNum, uID
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
        return Response(data={'code': 400, 'message': 'incomplete request data'}, status=status.HTTP_400_BAD_REQUEST)


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

    skip = max(count * (pageNum - 1), 0)
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

    try:
        # destructure params and typecast
        uID = params['uID']
    except:
        return Response(data={'code': 400, 'message': 'Incomplete request'}, status=status.HTTP_400_BAD_REQUEST)

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
    except (jwtLib.InvalidKeyError, jwtLib.InvalidSignatureError, jwtLib.InvalidTokenError) as err:
        return Response({ 'status': 401, 'message': 'Invalid auth token' }, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as err:
        print(f'uh oh: { err }')
        return Response({ 'status': 500, 'message': 'Error acquiring auth token' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        vacancy = reviewHelper.checkUserOwnsVacancy(vacancyId, jwt)

        if not vacancy:
            return Response({ 'status': 401, 'message': 'You do not have access to that vacancy' }, status=status.HTTP_401_UNAUTHORIZED)

        # get employer name
        employerDetails = EmployerDetails.objects.get(UserId__exact=jwt['id'])
        employer = employerDetails.CompanyName


        vacancy = { 'VacancyId': vacancy['VacancyId'], 'VacancyName': vacancy['VacancyName'], 'CompanyName': employer }
    except Exception as err:
        print(f'uh oh: { err }')
        return Response({ 'status': 500, 'message': 'Server error' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    try:
        applications = reviewHelper.getApplications(vacancyId)
    except Exception as err:
        print(f'uh oh: { err }')
        return Response({ 'status': 500, 'message': 'Error getting applications' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    applications['vacancy'] = vacancy

    return Response(applications)



@api_view(['PUT'])
def putReviewApplication(request, vacancyId, applicationId):
    # get jwt
    try:
        jwt = reviewHelper.extractJwt(request)
    except jwtLib.ExpiredSignatureError:
        return Response({ 'status': 401, 'message': 'Expired auth token' }, status=status.HTTP_401_UNAUTHORIZED)
    except (jwtLib.InvalidKeyError, jwtLib.InvalidSignatureError, jwtLib.InvalidTokenError) as err:
        return Response({ 'status': 401, 'message': 'Invalid auth token' }, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as err:
        print(f'uh oh: { err }')
        return Response({ 'status': 500, 'message': 'Error acquiring auth token' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    # check user owns vacancy
    try:
        vacancy = reviewHelper.checkUserOwnsVacancy(vacancyId, jwt)
    except Exception as err:
        print(f'uh oh: { err }')
        return Response({ 'status': 500, 'message': 'Server error' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    if not vacancy:
        return Response({ 'status': 401, 'message': 'You do not have access to that vacancy' }, status=status.HTTP_401_UNAUTHORIZED)
    

    # destructure params and typecast
    try:
        # new status = { defer, accept, reject }
        newStatus = request.data['setStatus']
    except:
        return Response(data={'code': 400, 'message': 'incomplete request data'}, status=status.HTTP_400_BAD_REQUEST)
    
    if newStatus not in ['defer', 'accept', 'reject']:
        return Response(data={'code': 400, 'message': 'invalid newStatus, must be one of "defer", "accept" or "reject"'}, status=status.HTTP_400_BAD_REQUEST)

    time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+0000')

    if newStatus == 'defer':
        updateValue = 'PENDING'
    elif newStatus == 'accept':
        updateValue = 'MATCHED'
    elif newStatus == 'reject':
        updateValue = 'REJECTED'


    try:
        application = Application.objects.get(pk=applicationId)

        application.ApplicationStatus = updateValue
        application.LastUpdated = time
        application.save()

        applicationSerializer = ApplicationSerializer(application)
        richApp = reviewHelper.pairApplications([applicationSerializer.data], SummaryProfileSerializer)[0]
    except Application.DoesNotExist:
        return Response(data={'code': 401, 'message': 'invalid application id'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as err:
        print(f'uh oh: { err }')
        return Response(data={'code': 500, 'message': 'server error getting application'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    try:
        nextApplication = reviewHelper.getNewApplication(vacancyId)
    except Exception as err:
        print(f'uh oh: { err }')
        return Response(data={'code': 500, 'message': 'server error getting next application'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    if nextApplication:
        return Response({ 'application': richApp, 'nextApplication': nextApplication['application'], 'nextProfile': nextApplication['profile'] })
    return Response({ 'application': richApp })



        
