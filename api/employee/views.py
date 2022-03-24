from math import ceil
from rest_framework import status
from django.db.models import Count, Q
from rest_framework.response import Response
from rest_framework.decorators import api_view
from employer.serializers import VacancySerializer
from employer.models import EmployerDetails, Vacancy


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
