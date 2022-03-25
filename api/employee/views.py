from doctest import DocFileSuite
import jwt as jwtLib
from math import ceil
from rest_framework import status
from employee.models import Application
from authentication import jwt as jwtHelper
from rest_framework.response import Response
from rest_framework.decorators import api_view
from employer.serializers import VacancySerializer
from employer.models import EmployerDetails, Vacancy
from employee.serializers import ApplicationSerializer



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
    except:
        return Response(data={'status': 400, 'message': 'incomplete request data'}, status=status.HTTP_400_BAD_REQUEST)

    # parse sort parameter into django sort parameter
    if sort == 'dateDesc':
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

    try:
        # get number of pages
        numVacancies = Vacancy.objects.filter(IsOpen__in = filterParam).count()
        pages = int(ceil(numVacancies / int(params['count'])))
        
        # deals with a lower number of pages than the current page
        while (pageNum - 1) * count >= numVacancies and pageNum > 1:
            pageNum -= 1

    except Exception as err:
        print(f'uh oh: { err }')
        return Response(data={'status': 500, 'message': 'Server error counting vacancies'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    skip = max(count * (pageNum - 1), 0)
    limit = count * pageNum

    try:
        # get vacancies
        vacanciesSet = Vacancy.objects.filter(
            IsOpen__in = filterParam
        ).order_by(sortParam)[skip:limit]

        vacancySerializer = VacancySerializer(vacanciesSet, many=True)
        vacancies = vacancySerializer.data

    except Exception as err:
        print(f'uh oh: { err }')
        return Response(data={'status': 500, 'message': 'Server error fetching vacancies'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

    try:
        # get company name
        for vacancy in vacancies:
            employerDetails = EmployerDetails.objects.get(UserId__exact = vacancy['UserId'])
            vacancy['CompanyName'] = employerDetails.CompanyName

    except EmployerDetails.DoesNotExist:
        return Response(data={'code': 500, 'message': 'error getting company name for vacancy'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as err:
        print(f'uh oh: { err }')
        return Response(data={'code': 500, 'message': 'Server error getting company name and stats'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # compile return data and send response
    returnData = {
        'numPages': pages,
        'vacancies': vacancies,
        'numVacancies': numVacancies
    }

    return Response(returnData)





@api_view(['GET'])
def getApplications(request):
    try:
        jwt = jwtHelper.extractJwt(request)
    except jwtLib.ExpiredSignatureError:
        return Response({ 'status': 401, 'message': 'Expired auth token' }, status=status.HTTP_401_UNAUTHORIZED)
    except (jwtLib.InvalidKeyError, jwtLib.InvalidSignatureError, jwtLib.InvalidTokenError) as err:
        return Response({ 'status': 401, 'message': 'Invalid auth token' }, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as err:
        print(f'uh oh: { err }')
        return Response({ 'status': 500, 'message': 'Error acquiring auth token' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # destructure params and typecast
    try:
        params = request.query_params

        sort = params['sort']
        filter = params['filter']
        count = int(params['count'])
        pageNum = int(params['pageNum'])

    except:
        return Response(data={'status': 400, 'message': 'incomplete request data'}, status=status.HTTP_400_BAD_REQUEST)


    # parse sort parameter into django sort parameter
    if sort == 'dateDesc':
        sortParam = '-LastUpdated'
    else:
        # dateAsc
        sortParam = 'LastUpdated'

    skip = max(count * (pageNum - 1), 0)
    limit = count * pageNum
    

    try:
        numApps = Application.objects.filter(UserId__exact = jwt['id']).count()
        numPages = ceil(numApps / count)

        # deals with a lower number of pages than the current page
        while (pageNum - 1) * count >= numApps and pageNum > 1:
            pageNum -= 1

        applicationSet = Application.objects.filter(
            UserId__exact = jwt['id']
        ).order_by(
            sortParam
        )[skip:limit]

        applications = ApplicationSerializer(applicationSet, many=True).data
    except Exception as err:
        print(f'uh oh: { err }')
        return Response({ 'status': 500, 'message': 'Error retrieving applications from the database' })

    pairedApplications = []
    
    try:
        for application in applications:
            vacancy = Vacancy.objects.get(pk = application['VacancyId'])
            employerDetails = EmployerDetails.objects.get(UserId__exact = vacancy.UserId)

            pair = { **application, 'VacancyId': vacancy.VacancyId, 'VacancyName': vacancy.VacancyName, 'CompanyName': employerDetails.CompanyName }
            pairedApplications.append(pair)

    except Vacancy.DoesNotExist:
        return Response({ 'status': 500, 'message': 'Error retrieving vacancy details from the database, possible database corruption' })
    except Exception as err:
        print(f'uh oh: { err }')
        return Response({ 'status': 500, 'message': 'Error retrieving vacancy details from the database' })



    return Response({ 'applications': pairedApplications, 'numPages': numPages })





@api_view(['GET'])
def getApplicationStats(request):
    try:
        jwt = jwtHelper.extractJwt(request)
    except jwtLib.ExpiredSignatureError:
        return Response({ 'status': 401, 'message': 'Expired auth token' }, status=status.HTTP_401_UNAUTHORIZED)
    except (jwtLib.InvalidKeyError, jwtLib.InvalidSignatureError, jwtLib.InvalidTokenError) as err:
        return Response({ 'status': 401, 'message': 'Invalid auth token' }, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as err:
        print(f'uh oh: { err }')
        return Response({ 'status': 500, 'message': 'Error acquiring auth token' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    try:
        numApps = Application.objects.filter(UserId__exact = jwt['id']).count()
        numPending = Application.objects.filter(UserId__exact = jwt['id'], ApplicationStatus__exact = 'PENDING').count()
        numMatches = Application.objects.filter(UserId__exact = jwt['id'], ApplicationStatus__exact = 'MATCHED').count()

        stats = {
            'total': numApps,
            'new': numPending,
            'matches': numMatches
        }

    except Exception as err:
        print(f'uh oh: { err }')
        return Response({ 'status': 500, 'message': 'Error retrieving application stats from the database' })

    
    return Response(stats)



@api_view(['GET'])
def getApplicationDetails(request, applicationId):
    try:
        # test jwt
        jwt = jwtHelper.extractJwt(request)
    except jwtLib.ExpiredSignatureError:
        return Response({ 'status': 401, 'message': 'Expired auth token' }, status=status.HTTP_401_UNAUTHORIZED)
    except (jwtLib.InvalidKeyError, jwtLib.InvalidSignatureError, jwtLib.InvalidTokenError) as err:
        return Response({ 'status': 401, 'message': 'Invalid auth token' }, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as err:
        print(f'uh oh: { err }')
        return Response({ 'status': 500, 'message': 'Error acquiring auth token' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        applicationSet = Application.objects.get(pk = applicationId, UserId__exact = jwt['id'])
        application = ApplicationSerializer(applicationSet).data
    except Application.DoesNotExist:
        return Response({ 'status': 401, 'message': 'You do not have access to that application' })
    except Exception as err:
        print(f'uh oh: { err }')
        return Response({ 'status': 500, 'message': 'Error getting application from the server' })

    try:
        vacancySet = Vacancy.objects.get(pk = application['VacancyId'])
        vacancy = VacancySerializer(vacancySet).data

        employerDetails = EmployerDetails.objects.get(UserId__exact = vacancySet.UserId)
        companyName = employerDetails.CompanyName

    except Application.DoesNotExist:
        return Response({ 'status': 500, 'message': 'Couldn\'t find vacancy details' })
    except Exception as err:
        print(f'uh oh: { err }')
        return Response({ 'status': 500, 'message': 'Error getting vacancy from the server' })

    return Response({ **application, **vacancy, 'CompanyName': companyName })