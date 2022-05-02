from ctypes.wintypes import tagSIZE
from math import ceil
from rest_framework import status
from employee.models import Favourite
from rest_framework.response import Response
from ..serializers import FavouriteSerializer
from rest_framework.decorators import api_view
from employer.serializers import VacancySerializer
from authentication.helpers import jwt as jwtHelper
from employer.models import EmployerDetails, Vacancy



@api_view(['GET'])
def getFavourites(request):
    
    jwt = jwtHelper.extractJwt(request)

    if type(jwt) is not dict:
        return jwt

    # destructure params and typecast
    try:
        params = request.query_params
        sort = params['sort']
        count = int(params['count'])
        pageNum = int(params['pageNum'])
        tags = params['tagsFilter']
    except:
        return Response(data={'status': 400, 'message': 'incomplete request data'}, status=status.HTTP_400_BAD_REQUEST)

    tagListInt = []

    if len(tags) < 1:
        tags = "null"

    if tags != "null":
        tagList = tags.split(',')

        for tag in tagList:
            tagListInt.append(int(tag))
    
    print(tagListInt)

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

    usingTags = False
    triedTags = False

    try:
        if tags != "null":
            favouriteSet = Favourite.objects.filter(
                UserId__exact = jwt['id'],
                VacancyId__Tags__contains = tagListInt
            )

            VacancyIds = []

            for fav in favouriteSet:
                VacancyIds.append(int(fav.VacancyId.VacancyId))

            if len(VacancyIds) > 0:
                usingTags = True
            else:
                triedTags = True

        if tags == "null" or usingTags == False:
            favouriteSet = Favourite.objects.filter(
                UserId__exact = jwt['id']
            )

            VacancyIds = []

            for fav in favouriteSet:
                VacancyIds.append(int(fav.VacancyId.VacancyId))

        # get number of pages
        numVacancies = len(VacancyIds)
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
        if usingTags == False:
            # get vacancies
            vacanciesSet = Vacancy.objects.filter(
                VacancyId__in = VacancyIds
            ).order_by(sortParam)[skip:limit]
        else:
            vacanciesSet = Vacancy.objects.filter(
                VacancyId__in = VacancyIds,
                Tags__contains = tagListInt
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
        'numVacancies': numVacancies,
        'triedTags': triedTags
    }

    return Response(returnData, status=status.HTTP_200_OK)



@api_view(['POST'])
def postFavourite(request):
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
        existingFavourites = Favourite.objects.filter(UserId__exact = jwt['id'], VacancyId__exact = vacancyId).count()

        if existingFavourites > 0:
            return Response({ 'status': 400, 'message': 'User has already favourited that vacancy' }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as err:
        print(f'uh oh: { err }')
        return Response({ 'status': 500, 'message': 'Server error checking request validity' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        newFavourite = {
            'VacancyId': vacancy.VacancyId,
            'UserId': jwt['id']
        }

        serializer = FavouriteSerializer(data = newFavourite)

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

@api_view(['DELETE'])
def deleteFavourite(request):
    jwt = jwtHelper.extractJwt(request)
    
    if type(jwt) is not dict:
        return jwt

    # destructure params
    try:
        vacancyId = request.data['VacancyId']
        userId = jwt['id']

        favourite = Favourite.objects.get(VacancyId__exact = vacancyId, UserId__exact = userId)

    except KeyError:
        return Response({ 'status': 400, 'message': 'Missing vacancy id from request' }, status=status.HTTP_400_BAD_REQUEST)
    except Favourite.DoesNotExist:
        return Response({ 'status': 401, 'message': 'Unauthorised favourite deletion' }, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as err:
        print(f'uh oh: { err }')
        return Response({ 'status': 500, 'message': 'Error getting vacancy details' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        favourite.delete()

        return Response(status=status.HTTP_200_OK)
    except Exception as err:
        return Response({ 'status': 500, 'message': 'Error deleting favourite' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
