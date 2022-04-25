from math import ceil
from django.test import TestCase
from employer.models import Vacancy, EmployerDetails
from employee.models import Application
from employee.serializers import ApplicationSerializer
from authentication.tests.jwtFuncs import createAccessToken

class getApplicationTests(TestCase):

    maxDiff = None
    userId = 2 # Adam
    vacancyId = 1
    jwt = createAccessToken(userId)
    applicationId = 1002
    fixtures = ['authentication/fixtures/testseed.json']

    def test_validRequestSortDateAscFilterAll(self):
        response = self.client.get('/applications/', { 'sort': 'dateAsc', 'count': 5, 'pageNum': 1, 'filter': 'all' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        applicationSet = Application.objects.filter(UserId__exact = self.userId, ApplicationStatus__in = ['MATCHED','PENDING','REJECTED']).order_by('LastUpdated')[0:5]
        numApps = Application.objects.filter(UserId__exact = self.userId).count()
        applications = ApplicationSerializer(applicationSet, many=True).data

        pairedApplications = []

        for app in applications:
            vacancy = Vacancy.objects.get(pk = app['VacancyId'])
            employerDetails = EmployerDetails.objects.get(UserId__exact = vacancy.UserId)

            pair = { **app, 'VacancyId': vacancy.VacancyId, 'VacancyName': vacancy.VacancyName, 'CompanyName': employerDetails.CompanyName }
            pairedApplications.append(pair)

        expectedData = {
            'applications': pairedApplications,
            'numPages': ceil(numApps / 5),
            'pageNum': 1,
            'numApps': numApps
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(expectedData, response.data)

    # Sort: dateDesc, Filter: matched
    def test_validRequestSortDateDescFilterMatched(self):
        response = self.client.get('/applications/', { 'sort': 'dateDesc', 'count': 5, 'pageNum': 1, 'filter': 'matched' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        applicationSet = Application.objects.filter(UserId__exact = self.userId, ApplicationStatus__in = ['MATCHED']).order_by('-LastUpdated')[0:5]
        numApps = Application.objects.filter(UserId__exact = self.userId, ApplicationStatus__in = ['MATCHED']).count()
        applications = ApplicationSerializer(applicationSet, many=True).data

        pairedApplications = []

        for app in applications:
            vacancy = Vacancy.objects.get(pk = app['VacancyId'])
            employerDetails = EmployerDetails.objects.get(UserId__exact = vacancy.UserId)

            pair = { **app, 'VacancyId': vacancy.VacancyId, 'VacancyName': vacancy.VacancyName, 'CompanyName': employerDetails.CompanyName }
            pairedApplications.append(pair)

        expectedData = {
            'applications': pairedApplications,
            'numPages': ceil(numApps / 5),
            'pageNum': 1,
            'numApps': numApps
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(expectedData, response.data)

    # Filter: pending, Incorrect Large Page Num
    def test_incorrectlyLargePageNumFilterPending(self):
        response = self.client.get('/applications/', { 'sort': 'dateAsc', 'count': 5, 'pageNum': 3, 'filter': 'pending' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        applicationSet = Application.objects.filter(UserId__exact = self.userId, ApplicationStatus__in = ['PENDING']).order_by('LastUpdated')[5:10]
        numApps = Application.objects.filter(UserId__exact = self.userId, ApplicationStatus__in = ['PENDING']).count()
        applications = ApplicationSerializer(applicationSet, many=True).data

        pairedApplications = []

        for app in applications:
            vacancy = Vacancy.objects.get(pk = app['VacancyId'])
            employerDetails = EmployerDetails.objects.get(UserId__exact = vacancy.UserId)

            pair = { **app, 'VacancyId': vacancy.VacancyId, 'VacancyName': vacancy.VacancyName, 'CompanyName': employerDetails.CompanyName }
            pairedApplications.append(pair)

        expectedData = {
            'applications': pairedApplications,
            'numPages': ceil(numApps / 5),
            'pageNum': 2,
            'numApps': numApps
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(expectedData, response.data)

    # Filter: rejected
    def test_validRequestFilterRejected(self):
        response = self.client.get('/applications/', { 'sort': 'dateAsc', 'count': 5, 'pageNum': 1, 'filter': 'rejected' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        applicationSet = Application.objects.filter(UserId__exact = self.userId, ApplicationStatus__in = ['REJECTED'])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['applications']), len(applicationSet))

    def test_missingParameters(self):
        response = self.client.get('/applications/', { }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 400)

    def test_expiredJWT(self):
        jwt = createAccessToken(self.userId, 'now')

        response = self.client.get('/applications/', { 'sort': 'titleAsc', 'count': 5, 'pageNum': 1, 'filter': 'all' }, **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Expired auth token')

    def test_invalidJWT(self):
        jwt = self.jwt[:-1]

        response = self.client.get('/applications/', { 'sort': 'titleAsc', 'count': 5, 'pageNum': 1, 'filter': 'all' }, **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Invalid auth token')

class getApplicationStatsTests(TestCase):

    userId = 2 # Adam
    vacancyId = 1
    jwt = createAccessToken(userId)
    applicationId = 1002
    fixtures = ['authentication/fixtures/testseed.json']
    
    def test_getApplicationsStats(self):
        response = self.client.get('/applications/stats/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        numApps = Application.objects.filter(
            UserId__exact = self.userId
        ).count()

        self.assertEquals(response.status_code, 200)
        self.assertEqual(response.data['total'], numApps)

    def test_expiredJWT(self):
        jwt = createAccessToken(self.userId, 'now')

        response = self.client.get('/applications/stats/', **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Expired auth token')

    def test_invalidJWT(self):
        jwt = self.jwt[:-1]

        response = self.client.get('/applications/stats/', **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Invalid auth token')

class getApplicationDetailsTests(TestCase):

    userId = 2 # Adam
    vacancyId = 1
    jwt = createAccessToken(userId)
    applicationId = 1002
    fixtures = ['authentication/fixtures/testseed.json']
    
    def test_validRequest(self):
        response = self.client.get(f'/applications/{ self.applicationId }/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 200)

    def test_unmatchedApplication(self):
        response = self.client.get(f'/applications/{ 1039 }/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.data['status'], 400)
        self.assertEqual(response.data['message'], 'You have not matched with that vacancy.')

    def test_noApplicationExists(self):
        response = self.client.get(f'/applications/{ 9999 }/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'You do not have access to that application')

    def test_expiredJWT(self):
        jwt = createAccessToken(self.userId, 'now')

        response = self.client.get(f'/applications/{ self.applicationId }/', **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Expired auth token')

    def test_invalidJWT(self):
        jwt = self.jwt[:-1]

        response = self.client.get(f'/applications/{ self.applicationId }/', **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Invalid auth token')

class postApplicationTests(TestCase):

    userId = 2 # Adam
    vacancyId = 1
    jwt = createAccessToken(userId)
    applicationId = 1002
    fixtures = ['authentication/fixtures/testseed.json']

    # Valid Request
    def test_validRequest(self):
        response = self.client.post('/vacancy/apply/', { 'VacancyId': self.vacancyId}, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 201)

    def test_invalidVacancy(self):
        response = self.client.post('/vacancy/apply/', { 'VacancyId': 2}, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 400)

    def test_missingParameters(self):
        response = self.client.post('/vacancy/apply/', { }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 400)

    def test_expiredJWT(self):
        jwt = createAccessToken(self.userId, 'now')

        response = self.client.post('/vacancy/apply/', { 'VacancyId': self.vacancyId }, **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['message'], 'Expired auth token')

    def test_invalidJWT(self):
        jwt = self.jwt[:-1]

        response = self.client.post('/vacancy/apply/', { 'VacancyId': self.vacancyId }, **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['message'], 'Invalid auth token')

class deleteApplicationTests(TestCase):
    
    userId = 2 # Adam
    vacancyId = 1
    jwt = createAccessToken(userId)
    applicationId = 1002
    fixtures = ['authentication/fixtures/testseed.json']

    def test_validRequest(self):
        originalSet = Application.objects.filter(
            VacancyId__exact = self.vacancyId
        ).count()

        response = self.client.delete(f'/applications/delete/{ self.applicationId }/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        newSet = Application.objects.filter(
            VacancyId__exact = self.vacancyId
        ).count()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(originalSet - 1, newSet)

    def test_invalidRequest(self):
        applicationId = 1017
        response = self.client.delete(f'/applications/delete/{ applicationId }/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 401)

    def test_expiredJWT(self):
        jwt = createAccessToken(self.userId, 'now')

        response = self.client.delete(f'/applications/delete/{ self.applicationId }/', **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Expired auth token')

    def test_invalidJWT(self):
        jwt = self.jwt[:-1]

        response = self.client.delete(f'/applications/delete/{ self.applicationId }/', **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Invalid auth token')