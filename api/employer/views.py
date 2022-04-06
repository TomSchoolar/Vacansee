from math import ceil
from datetime import datetime
from rest_framework import status
from django.db.models import Count, Q
from employee.models import Application
from .serializers import VacancySerializer
from rest_framework.response import Response
from .models import EmployerDetails, Vacancy
from rest_framework.decorators import api_view
from authentication.helpers import jwt as jwtHelper
from employee.serializers import ApplicationSerializer, SummaryProfileSerializer
from employer.helpers import getIndex as indexHelper, getReview as reviewHelper, getMatch as matchHelper



@api_view(['GET'])
def getIndex(request):
    jwt = jwtHelper.extractJwt(request)

    if type(jwt) is not dict:
        return jwt

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
                UserId__exact = uID,
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

    try:
        # get company name
        employerDetails = EmployerDetails.objects.get(UserId__exact = uID)
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
    
    jwt = jwtHelper.extractJwt(request)

    if type(jwt) is not dict:
        return jwt

    try:
        vacancy = reviewHelper.checkUserOwnsVacancy(vacancyId, jwt)

        # get employer name
        employerDetails = EmployerDetails.objects.get(UserId__exact=jwt['id'])
        employer = employerDetails.CompanyName


        vacancy = { 'VacancyId': vacancy['VacancyId'], 'VacancyName': vacancy['VacancyName'], 'CompanyName': employer }
    except Vacancy.DoesNotExist:
        return Response({ 'status': 401, 'message': 'You do not have access to that vacancy' }, status=status.HTTP_401_UNAUTHORIZED)
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
    jwt = jwtHelper.extractJwt(request)

    if type(jwt) is not dict:
        return jwt
    
    # check user owns vacancy
    try:
        reviewHelper.checkUserOwnsVacancy(vacancyId, jwt)
    except Vacancy.DoesNotExist:
        return Response({ 'status': 401, 'message': 'You do not have access to that vacancy' }, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as err:
        print(f'uh oh: { err }')
        return Response({ 'status': 500, 'message': 'Server error' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    # destructure params and typecast
    try:
        # new status = { defer, accept, reject }
        newStatus = request.data['setStatus']
    except:
        return Response(data={'status': 400, 'message': 'incomplete request data'}, status=status.HTTP_400_BAD_REQUEST)
    
    if newStatus not in ['defer', 'accept', 'reject']:
        return Response(data={'status': 400, 'message': 'invalid setStatus, must be one of "defer", "accept" or "reject"'}, status=status.HTTP_400_BAD_REQUEST)

    time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+0000')

    if newStatus == 'defer':
        updateValue = 'PENDING'
    elif newStatus == 'accept':
        updateValue = 'MATCHED'
    elif newStatus == 'reject':
        updateValue = 'REJECTED'


    try:
        application = Application.objects.get(pk=applicationId, VacancyId__exact = vacancyId)

        application.ApplicationStatus = updateValue
        application.LastUpdated = time
        application.save()

        applicationSerializer = ApplicationSerializer(application)
        richApp = reviewHelper.pairApplications([applicationSerializer.data], SummaryProfileSerializer)[0]
    except Application.DoesNotExist:
        return Response(data={'status': 401, 'message': 'invalid application id'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as err:
        print(f'uh oh: { err }')
        return Response(data={'status': 500, 'message': 'server error getting application'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    try:
        nextApplication = reviewHelper.getNewApplication(vacancyId)
    except Exception as err:
        print(f'uh oh: { err }')
        return Response(data={'status': 500, 'message': 'server error getting next application'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    if nextApplication:
        return Response({ 'application': richApp, 'nextApplication': nextApplication['application'], 'nextProfile': nextApplication['profile'] })
    return Response({ 'application': richApp })



@api_view(['GET'])
def getMatchVacancies(request):

    jwt = jwtHelper.extractJwt(request)

    if type(jwt) is not dict:
        return jwt

    params = request.query_params

    try:
        uID = params['uID']
        sort = params['sort']
        sortByNum = False
    except:
        return Response(data={'code': 400, 'message': 'incomplete request data'}, status=status.HTTP_400_BAD_REQUEST)

    if sort == 'matchesDesc':
        sortByNum = True
        sortParam = '-Created' #delete
    elif sort == 'dateDesc':
        sortParam = '-Created'
    elif sort == 'dateAsc':
        sortParam = 'Created'
    elif sort == 'titleAsc':
        sortParam = 'VacancyName'
    else:
        sortParam = '-VacancyName'

    numVacancies = Vacancy.objects.filter(
        UserId__exact = uID,
    ).count()

    #add if-else for sortByNum
    vacanciesSet = Vacancy.objects.filter(
        UserId__exact = uID,
    ).order_by(sortParam)

    vacancySerializer = VacancySerializer(vacanciesSet, many=True)
    vacancies = vacancySerializer.data

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
        uID = params['uID']
        vID = params['vID']
        sort = params['sort']
    except:
        return Response(data={'code': 400, 'message': 'incomplete request data'}, status=status.HTTP_400_BAD_REQUEST)

    # add sorting

    #matches = matchHelper.getMatches(vID)
    matches = reviewHelper.getApplications(vID)

    numMatches = Application.objects.filter(
        VacancyId__exact = vID,
        ApplicationStatus__exact = 'MATCHED'
    ).count()

    returnData = {
        'matches': matches['matches'],
        #'applications': matches['applications']
        'numMatches': numMatches
    }

    return Response(returnData)



@api_view(['GET'])
def getCard(request):

    jwt = jwtHelper.extractJwt(request)

    if type(jwt) is not dict:
        return jwt

    params = request.query_params

    try:
        uID = params['uID']
    except:
        return Response(data={'code': 400, 'message': 'incomplete request data'}, status=status.HTTP_400_BAD_REQUEST)

    # add sorting

    #matches = matchHelper.getMatches(vID)
    #matches = reviewHelper.getApplications(vID)
    details = matchHelper.getDetails(uID)

    returnData = {
        'details': details
    }

    return Response(returnData)