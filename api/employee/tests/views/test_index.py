from math import ceil
from django.test import TestCase
from employer.serializers import VacancySerializer, EmployerDetails
from employer.models import Vacancy
from authentication.tests.jwtFuncs import createAccessToken
from employee.models import Favourite, Reject, Application



class applicationTestCase(TestCase):

    fixtures = ['authentication/fixtures/testseed.json']
    jwt = createAccessToken(1019)

    def getVacancyList(self):

        vacancyList = []

        favouriteSet = Favourite.objects.filter(
            UserId__exact = 1019
        )

        rejectSet = Reject.objects.filter(
            UserId__exact = 1019
        )

        applicationSet = Application.objects.filter(
            UserId__exact = 1019
        )

        for fav in favouriteSet:
            vacancyList.append(fav.VacancyId.VacancyId)

        for rej in rejectSet:
            vacancyList.append(rej.VacancyId.VacancyId)

        for app in applicationSet:
            vacancyList.append(app.VacancyId.VacancyId)

        return vacancyList

    def test_validRequestSortTitleAscFilterAll(self):
        response = self.client.get('/vacancy/', { 'uID':1019, 'sort':'titleAsc', 'count':5, 'pageNum':1, 'filter':'all' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

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
        response = self.client.get('/vacancy/', { 'uID':1019, 'sort':'titleDesc', 'count':5, 'pageNum':1, 'filter':'closed' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

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
        response = self.client.get('/vacancy/', { 'uID':1019, 'sort':'dateDesc', 'count':5, 'pageNum':1, 'filter':'active' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

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
        response = self.client.get('/vacancy/', { 'uID':1019, 'sort':'dateAsc', 'count':5, 'pageNum':5, 'filter':'all' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        vacancyList = self.getVacancyList()

        numVacancies = Vacancy.objects.filter(IsOpen__in = [True, False]).exclude(VacancyId__in = vacancyList).count()

        vacanciesSet = Vacancy.objects.filter(IsOpen__in = [True, False]).exclude(VacancyId__in = vacancyList).order_by('Created')[10:15] 
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
        response = self.client.get('/vacancy/', { }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 400)

    def test_expiredJWT(self):
        jwt = createAccessToken(self.jwt, 'now')

        response = self.client.get('/vacancy/', { 'sort':'titleAsc', 'count':5, 'pageNum':1, 'filter':'all' }, **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Expired auth token')

    def test_invalidJWT(self):
        jwt = self.jwt[:-1]

        response = self.client.get('/vacancy/', { 'sort':'titleAsc', 'count':5, 'pageNum':1, 'filter':'all' }, **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Invalid auth token')