from math import ceil
from django.test import TestCase
from employee.models import Favourite
from employer.serializers import VacancySerializer
from employer.models import Vacancy, EmployerDetails
from authentication.tests.jwtFuncs import createAccessToken

class getFavouritesTests(TestCase):

    userId = 2
    jwt = createAccessToken(userId)
<<<<<<< HEAD
=======

    fixtures = ['authentication/fixtures/testseed.json']
>>>>>>> b62fb52695f4f133c95ea0a7f81aa48e44cc993f

    fixtures = ['authentication/fixtures/testseed.json']


    def test_validRequestSortDateDesc(self):
        response = self.client.get('/v1/favourites/', { 'sort': 'dateDesc', 'count': 5, 'pageNum': 1, 'tagsFilter': 'null', 'searchValue': '' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        favouriteSet = Favourite.objects.filter(UserId__exact = self.userId)
        vacancyIds = []
        for fav in favouriteSet:
            vacancyIds.append(int(fav.VacancyId.VacancyId))

        vacanciesSet = Vacancy.objects.filter(VacancyId__in = vacancyIds).order_by('-Created')[0:5]
        numVacancies = Vacancy.objects.filter(VacancyId__in = vacancyIds).count()
        vacancies = VacancySerializer(vacanciesSet, many=True).data

        for vacancy in vacancies:
            employerDetails = EmployerDetails.objects.get(UserId__exact = vacancy['UserId'])
            vacancy['CompanyName'] = employerDetails.CompanyName

        expectedData = {
            'numPages': ceil(numVacancies / 5),
            'vacancies': vacancies,
            'numVacancies': numVacancies,
            'triedTags': False
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(expectedData, response.data)



    def test_validRequestSortDateAsc(self):
        response = self.client.get('/v1/favourites/', { 'sort': 'dateAsc', 'count': 5, 'pageNum': 1, 'tagsFilter': 'null', 'searchValue': '' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})
        
        favouriteSet = Favourite.objects.filter(UserId__exact = self.userId)
        vacancyIds = []
        for fav in favouriteSet:
            vacancyIds.append(int(fav.VacancyId.VacancyId))

        vacanciesSet = Vacancy.objects.filter(VacancyId__in = vacancyIds).order_by('Created')[0:5]
        numVacancies = Vacancy.objects.filter(VacancyId__in = vacancyIds).count()
        vacancies = VacancySerializer(vacanciesSet, many=True).data

        for vacancy in vacancies:
            employerDetails = EmployerDetails.objects.get(UserId__exact = vacancy['UserId'])
            vacancy['CompanyName'] = employerDetails.CompanyName

        expectedData = {
            'numPages': ceil(numVacancies / 5),
            'vacancies': vacancies,
            'numVacancies': numVacancies,
            'triedTags': False
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(expectedData, response.data)



    def test_validRequestSortTitleAsc(self):
        response = self.client.get('/v1/favourites/', { 'sort': 'titleAsc', 'count': 5, 'pageNum': 1, 'tagsFilter': 'null', 'searchValue': '' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})
        
        favouriteSet = Favourite.objects.filter(UserId__exact = self.userId)
        vacancyIds = []
        for fav in favouriteSet:
            vacancyIds.append(int(fav.VacancyId.VacancyId))

        vacanciesSet = Vacancy.objects.filter(VacancyId__in = vacancyIds).order_by('VacancyName')[0:5]
        numVacancies = Vacancy.objects.filter(VacancyId__in = vacancyIds).count()
        vacancies = VacancySerializer(vacanciesSet, many=True).data

        for vacancy in vacancies:
            employerDetails = EmployerDetails.objects.get(UserId__exact = vacancy['UserId'])
            vacancy['CompanyName'] = employerDetails.CompanyName

        expectedData = {
            'numPages': ceil(numVacancies / 5),
            'vacancies': vacancies,
            'numVacancies': numVacancies,
            'triedTags': False
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(expectedData, response.data)



    def test_incorrectlyLargePageNumSortTitleDesc(self):
        response = self.client.get('/v1/favourites/', { 'sort': 'titleDesc', 'count': 5, 'pageNum': 3, 'tagsFilter': 'null', 'searchValue': '' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        favouriteSet = Favourite.objects.filter(UserId__exact = self.userId)
        vacancyIds = []
        for fav in favouriteSet:
            vacancyIds.append(int(fav.VacancyId.VacancyId))

        vacanciesSet = Vacancy.objects.filter(VacancyId__in = vacancyIds).order_by('-VacancyName')[5:10]
        numVacancies = Vacancy.objects.filter(VacancyId__in = vacancyIds).count()
        vacancies = VacancySerializer(vacanciesSet, many=True).data

        for vacancy in vacancies:
            employerDetails = EmployerDetails.objects.get(UserId__exact = vacancy['UserId'])
            vacancy['CompanyName'] = employerDetails.CompanyName

        expectedData = {
            'numPages': ceil(numVacancies / 5),
            'vacancies': vacancies,
            'numVacancies': numVacancies,
            'triedTags': False
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(expectedData, response.data)



    def test_validRequestTagSearch(self):
        response = self.client.get('/v1/favourites/', { 'sort': 'titleAsc', 'count': 5, 'pageNum': 1, 'tagsFilter': '3', 'searchValue': '' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})
        
        favouriteSet = Favourite.objects.filter(UserId__exact = self.userId)
        vacancyIds = []
        for fav in favouriteSet:
            vacancyIds.append(int(fav.VacancyId.VacancyId))
        
        vacanciesSet = Vacancy.objects.filter(VacancyId__in = vacancyIds, Tags__contains = [3]).order_by('VacancyName')[0:5]
        numVacancies = Vacancy.objects.filter(VacancyId__in = vacancyIds, Tags__contains = [3]).count()
        vacancies = VacancySerializer(vacanciesSet, many=True).data

        for vacancy in vacancies:
            employerDetails = EmployerDetails.objects.get(UserId__exact = vacancy['UserId'])
            vacancy['CompanyName'] = employerDetails.CompanyName

        expectedData = {
            'numPages': ceil(numVacancies / 5),
            'vacancies': vacancies,
            'numVacancies': numVacancies,
            'triedTags': False
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(expectedData, response.data)



    def test_validRequestSearchBar(self):
        response = self.client.get('/v1/favourites/', { 'sort': 'titleAsc', 'count': 5, 'pageNum': 1, 'tagsFilter': 'null', 'searchValue': 't' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 200)



    def test_missingParameters(self):
        response = self.client.get('/v1/favourites/', { }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 400)



    def test_expiredJWT(self):
        jwt = createAccessToken(self.userId, 'now')

        response = self.client.get('/v1/favourites/', { 'sort': 'titleAsc', 'count': 5, 'pageNum': 1, 'tagsFilter': 'null', 'searchValue': '' }, **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Expired auth token')



    def test_invalidJWT(self):
        jwt = self.jwt[:-1]

        response = self.client.get('/v1/favourites/', { 'sort': 'titleAsc', 'count': 5, 'pageNum': 1, 'tagsFilter': 'null', 'searchValue': '' }, **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Invalid auth token')



class postFavouritesTests(TestCase):
    
    vacId = 1002
    userId = 2
    jwt = createAccessToken(userId)

    fixtures = ['authentication/fixtures/testseed.json']


    def test_validRequest(self):
        response = self.client.post(f'/v1/vacancies/{ self.vacId }/favourite/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 201)      



    def test_invalidVacancy(self):
        response = self.client.post(f'/v1/vacancies/{ 9999 }/favourite/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.data['status'], 400)
        self.assertEqual(response.data['message'], 'That vacancy is not open for applications')
    


    def test_repeatedFavourite(self):
        response = self.client.post(f'/v1/vacancies/{ 1003 }/favourite/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.data['status'], 400)
        self.assertEqual(response.data['message'], 'User has already favourited that vacancy')



    def test_expiredJWT(self):
        jwt = createAccessToken(self.userId, 'now')

        response = self.client.post(f'/v1/vacancies/{ self.vacId }/favourite/', **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Expired auth token')



    def test_invalidJWT(self):
        jwt = self.jwt[:-1]

        response = self.client.post(f'/v1/vacancies/{ self.vacId}/favourite/', **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Invalid auth token')



class deleteFavouriteTests(TestCase):

    vacId = 1007
    userId = 1
    jwt = createAccessToken(userId)
    
    fixtures = ['authentication/fixtures/testseed.json']


    def test_validRequest(self):
        response = self.client.delete(
                    f'/v1/vacancies/{ self.vacId }/unfavourite/',
                    **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 200)



    def test_invalidFavourite(self):
        invalidVacancyId = 1000

        response = self.client.delete(
                    f'/v1/vacancies/{ invalidVacancyId }/unfavourite/',
                    **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Unauthorised favourite deletion')



    def test_expiredJWT(self):
        jwt = createAccessToken(self.userId, 'now')

        response = self.client.delete(f'/v1/vacancies/{ self.vacId }/unfavourite/', **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Expired auth token')



    def test_invalidJWT(self):
        jwt = self.jwt[:-1]

        response = self.client.delete(f'/v1/vacancies/{ self.vacId }/unfavourite/', **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Invalid auth token')