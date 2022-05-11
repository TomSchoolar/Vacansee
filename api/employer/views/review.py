from datetime import datetime
from rest_framework import status
from employee.models import Application
from rest_framework.response import Response
from ..models import EmployerDetails, Vacancy
from rest_framework.decorators import api_view
from authentication.helpers import jwt as jwtHelper
from employer.helpers import getReview as reviewHelper
from employee.serializers import ApplicationSerializer, SummaryProfileSerializer



@api_view(['GET'])
def getReview(request, vacancyId):
    # get jwt
    
    jwt = jwtHelper.extractJwt(request)

    if type(jwt) is not dict:
        return jwt

    params = request.query_params

    try:
        searchValue = params['searchValue']
    except:
        return Response(data={'code': 400, 'message': 'incomplete request data'}, status=status.HTTP_400_BAD_REQUEST)

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
        applications = reviewHelper.getApplications(vacancyId, "FirstNameAsc", searchValue)
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
        return Response(data={'status': 404, 'message': 'invalid application id'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as err:
        print(f'uh oh: { err }')
        return Response(data={'status': 500, 'message': 'server error getting application'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    try:
        nextApplication = reviewHelper.getNewApplication(vacancyId)
    except Exception as err:
        print(f'uh oh: { err }')
        return Response(data={'status': 500, 'message': 'server error getting next application'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    if nextApplication:
        return Response({ 'application': richApp, 'nextApplication': nextApplication['application'], 'nextProfile': nextApplication['profile'] }, status=status.HTTP_200_OK)
    return Response({ 'application': richApp }, status=status.HTTP_200_OK)