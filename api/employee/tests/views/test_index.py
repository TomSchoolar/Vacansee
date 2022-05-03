from math import ceil
from django.test import TestCase
from employer.serializers import VacancySerializer, EmployerDetails
from employer.models import Vacancy
from authentication.tests.jwtFuncs import createAccessToken
from employee.models import Favourite, Reject, Application



class applicationTestCase(TestCase):

    fixtures = ['authentication/fixtures/testseed.json']

    userId = 1 # Tom
    jwt = createAccessToken(userId)

    def getVacancyList(self):

        vacancyList = []

        favouriteSet = Favourite.objects.filter(
            UserId__exact = self.userId
        )

        rejectSet = Reject.objects.filter(
            UserId__exact = self.userId
        )

        applicationSet = Application.objects.filter(
            UserId__exact = self.userId
        )

        for fav in favouriteSet:
            vacancyList.append(fav.VacancyId.VacancyId)

        for rej in rejectSet:
            vacancyList.append(rej.VacancyId.VacancyId)

        for app in applicationSet:
            vacancyList.append(app.VacancyId.VacancyId)

        return vacancyList

    def test_validRequestSortTitleAscFilterAll(self):
        response = self.client.get('/v1/vacancies/', { 'sort': 'titleAsc', 'count': 5, 'pageNum': 1, 'filter': 'all' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        vacancyList = self.getVacancyList()

        numVacancies = Vacancy.objects.filter(IsOpen__in = [True, False]).exclude(VacancyId__in = vacancyList).count()

        vacanciesSet = Vacancy.objects.filter(IsOpen__in = [True, False]).exclude(VacancyId__in = vacancyList).order_by('VacancyName')[0:5] 
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

    def test_validRequestSortTitleDescFilterClosed(self):
        response = self.client.get('/v1/vacancies/', { 'sort': 'titleDesc', 'count': 5, 'pageNum': 1, 'filter': 'closed' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        vacancyList = self.getVacancyList()

        numVacancies = Vacancy.objects.filter(IsOpen__in = [False]).exclude(VacancyId__in = vacancyList).count()

        vacanciesSet = Vacancy.objects.filter(IsOpen__in = [False]).exclude(VacancyId__in = vacancyList).order_by('-VacancyName')[0:5] 
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

    def test_validRequestSortDateDescFilterActive(self):
        response = self.client.get('/v1/vacancies/', { 'sort': 'dateDesc', 'count': 5, 'pageNum': 1, 'filter': 'active' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        vacancyList = self.getVacancyList()

        numVacancies = Vacancy.objects.filter(IsOpen__in = [True]).exclude(VacancyId__in = vacancyList).count()

        vacanciesSet = Vacancy.objects.filter(IsOpen__in = [True]).exclude(VacancyId__in = vacancyList).order_by('-Created')[0:5] 
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

    def test_incorrectlyLargePageNumSortDateAsc(self):
        response = self.client.get('/v1/vacancies/', { 'sort': 'dateAsc', 'count': 5, 'pageNum': 5, 'filter': 'all' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        vacancyList = self.getVacancyList()

        numVacancies = Vacancy.objects.filter(IsOpen__in = [True, False]).exclude(VacancyId__in = vacancyList).count()

        vacanciesSet = Vacancy.objects.filter(IsOpen__in = [True, False]).exclude(VacancyId__in = vacancyList).order_by('Created')[:5] 
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
        response = self.client.get('/v1/vacancies/', { }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 400)

    def test_expiredJWT(self):
        jwt = createAccessToken(self.userId, 'now')

        response = self.client.get('/v1/vacancies/', { 'sort': 'titleAsc', 'count': 5, 'pageNum': 1, 'filter': 'all' }, **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Expired auth token')

    def test_invalidJWT(self):
        jwt = self.jwt[:-1]

        response = self.client.get('/v1/vacancies/', { 'sort': 'titleAsc', 'count': 5, 'pageNum': 1, 'filter': 'all' }, **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Invalid auth token')