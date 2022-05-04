from math import ceil
from rest_framework import status
from django.db.models import Count, Q
from ..serializers import RejectSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from employer.serializers import VacancySerializer
from authentication.helpers import jwt as jwtHelper
from employer.models import EmployerDetails, Vacancy
from employee.models import Application, Favourite, Reject



@api_view(['GET'])
def getIndex(request):

    params = request.query_params

    jwt = jwtHelper.extractJwt(request)

    if type(jwt) is not dict:
        try:
            noAuth = params['noAuth']

            if not noAuth or noAuth.lower() != 'true':
                return jwt
            else:
                return getIndexNoAuth(request)
        except:
            return jwt


    # get query params: sort, count, filter, pageNum

    # destructure params and typecast
    try:
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

        vacancyList = []

        favouriteSet = Favourite.objects.filter(
            UserId__exact = jwt['id']
        )

        rejectSet = Reject.objects.filter(
            UserId__exact = jwt['id']
        )

        applicationSet = Application.objects.filter(
            UserId__exact = jwt['id']
        )

        for fav in favouriteSet:
            vacancyList.append(fav.VacancyId.VacancyId)

        for rej in rejectSet:
            vacancyList.append(rej.VacancyId.VacancyId)

        for app in applicationSet:
            vacancyList.append(app.VacancyId.VacancyId)

        numVacancies = Vacancy.objects.filter(
            IsOpen__in = filterParam
        ).exclude(
            VacancyId__in = vacancyList
        ).count()

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
        ).exclude(
            VacancyId__in = vacancyList
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

    return Response(returnData, status=status.HTTP_200_OK)



def getIndexNoAuth(request):
    # get requested number of the most popular vacancies without auth

    # destructure params and typecast
    try:
        count = int(request.query_params['count'])
    except:
        return Response(data={'status': 400, 'message': 'request params missing valid count value'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # sort by the number of applications referencing vacancy
        vacanciesSet = Vacancy.objects.filter(
            IsOpen__exact = True
        ).annotate(
            applicationCount = Count('application', filter=Q(application__ApplicationStatus__exact='PENDING'))
        ).order_by(
            '-applicationCount'
        )[:count]

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

    
    returnData = {
        'vacancies': vacancies
    }

    if len(vacancies) < count:
        returnData['message'] = 'There are not the requested number of vacancies open for applications.'

    return Response(returnData, status=status.HTTP_200_OK)





@api_view(['POST'])
def postReject(request):
    jwt = jwtHelper.extractJwt(request)
    
    if type(jwt) is not dict:
        return jwt

    try:
        vacancyId = request.data['VacancyId']

        vacancy = Vacancy.objects.get(pk = vacancyId, IsOpen__exact = True)

    except KeyError:
        return Response({ 'status': 400, 'message': 'Missing vacancy id from request' }, status=status.HTTP_400_BAD_REQUEST)
    except Vacancy.DoesNotExist:
        return Response({ 'status': 400, 'message': 'That vacancy is not open for applications' }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as err:
        print(f'uh oh: { err }')
        return Response({ 'status': 500, 'message': 'Error getting vacancy details' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        newReject = {
            'VacancyId': vacancy.VacancyId,
            'UserId': jwt['id']
        }

        serializer = RejectSerializer(data = newReject)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()        
    
    except Exception as err:
        print(f'uh oh: { err }')
        return Response({ 'status': 500, 'message': 'Error while saving favourite' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    try:
        newVacancySet = Vacancy.objects.filter(IsOpen__exact = True)
        newVacancy = False

        for vac in newVacancySet:
            if vac.VacancyId != vacancy.VacancyId:
                newVacancy = VacancySerializer(vac).data
                break

        employerDetails = EmployerDetails.objects.get(UserId__exact = newVacancy['UserId'])
        newVacancy['CompanyName'] = employerDetails.CompanyName
        
    except Exception as err:
        print(f'uh oh: { err }')
        return Response({ 'status': 500, 'message': 'Error getting next vacancy' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(newVacancy, status=status.HTTP_201_CREATED)