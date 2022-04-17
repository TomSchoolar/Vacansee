from math import ceil
from django.test import TestCase
from employer.serializers import VacancySerializer
from employer.models import Vacancy, EmployerDetails
from employee.models import Favourite
from authentication.tests.jwtFuncs import createAccessToken

class getFavouritesTests(TestCase):

    userId = 2
    jwt = createAccessToken(userId)
    fixtures = ['authentication/fixtures/testseed.json']

    def test_validRequestSortDateDesc(self):
        response = self.client.get('/favourites/', { 'sort':'dateDesc', 'count':5, 'pageNum':1 }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

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
            'numVacancies': numVacancies
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(expectedData, response.data)


    def test_validRequestSortDateAsc(self):
        response = self.client.get('/favourites/', { 'sort':'dateAsc', 'count':5, 'pageNum':1 }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})
        
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
            'numVacancies': numVacancies
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(expectedData, response.data)


    def test_validRequestSortTitleAsc(self):
        response = self.client.get('/favourites/', { 'sort':'titleAsc', 'count':5, 'pageNum':1 }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})
        
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
            'numVacancies': numVacancies
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(expectedData, response.data)


    def test_incorrectlyLargePageNumSortTitleDesc(self):
        response = self.client.get('/favourites/', { 'sort':'titleDesc', 'count':5, 'pageNum':3 }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

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
            'numVacancies': numVacancies
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(expectedData, response.data)

    def test_missingParameters(self):
        response = self.client.get('/favourites/', { }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 400)

    def test_expiredJWT(self):
        jwt = createAccessToken(self.userId, 'now')

        response = self.client.get('/favourites/', { 'sort':'titleAsc', 'count':5, 'pageNum':1 }, **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Expired auth token')

    def test_invalidJWT(self):
        jwt = self.jwt[:-1]

        response = self.client.get('/favourites/', { 'sort':'titleAsc', 'count':5, 'pageNum':1 }, **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Invalid auth token')

class postFavouritesTests(TestCase):
    
    vacId = 1000
    userId = 2
    jwt = createAccessToken(userId)
    fixtures = ['authentication/fixtures/testseed.json']
    
    def test_validRequest(self):
        response = self.client.post('/vacancy/fav/', { 'VacancyId': self.vacId }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 201)      

    def test_invalidVacancy(self):
        response = self.client.post('/vacancy/fav/', { 'VacancyId': 9999 }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.data['status'], 400)
        self.assertEqual(response.data['message'], 'That vacancy is not open for applications')

    def test_missingParameters(self):
        response = self.client.post('/vacancy/fav/', { }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 400)

    def test_expiredJWT(self):
        jwt = createAccessToken(self.userId, 'now')

        response = self.client.post('/vacancy/fav/', { 'VacancyId': self.vacId }, **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Expired auth token')

    def test_invalidJWT(self):
        jwt = self.jwt[:-1]

        response = self.client.post('/vacancy/fav/', { 'VacancyId': self.vacId }, **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Invalid auth token')