from math import ceil
from django.test import TestCase
from employer.models import Vacancy
from django.db.models import Count, Q
from employer.serializers import VacancySerializer
from employer.helpers.getIndex import getVacancyStats
from authentication.tests.jwtFuncs import createAccessToken


class indexTestCase(TestCase):

    userId = 4
    jwt = createAccessToken(userId)
    fixtures = ['authentication/fixtures/testseed.json']

    # GET INDEX TESTS

    def test_validRequestSortNewApplications(self):
        # User: Sabah
        response = self.client.get('/v1/e/vacancies/', { 'sort': 'newApps', 'filter': 'all', 'pageNum': 1, 'count': '10' }, **{ 'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }' })
        
        vacancySet = Vacancy.objects.filter(
                UserId__exact = 4
            ).annotate( 
                applicationCount = Count('application', filter=Q(application__ApplicationStatus__exact='PENDING')) 
            ).order_by( 
                '-applicationCount' 
            )
        vacancies = VacancySerializer(vacancySet, many=True).data
        vacanciesCount = vacancySet = Vacancy.objects.filter(UserId__exact = 4).count()

        getVacancyStats(vacancies)

        expectedData = {
            'vacancies': vacancies,
            'numPages': ceil(len(vacancies) / 10),
            'numVacancies': vacanciesCount,
            'companyName': 'Facebook'
        }

        self.assertEquals(response.status_code, 200)
        self.assertDictEqual(expectedData, response.data)



    def test_validRequestSortDateAsc(self):
        # User: Sabah
        response = self.client.get('/v1/e/vacancies/', { 'sort': 'dateAsc', 'filter': 'all', 'pageNum': 1, 'count': '10' }, **{ 'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }' })
        
        vacancySet = Vacancy.objects.filter(
                UserId__exact = 4
            ).annotate( 
                applicationCount = Count('application', filter=Q(application__ApplicationStatus__exact='PENDING')) 
            ).order_by( 
                'Created' 
            )
        vacancies = VacancySerializer(vacancySet, many=True).data

        getVacancyStats(vacancies)

        expectedData = {
            'vacancies': vacancies,
            'numPages': ceil(len(vacancies) / 10),
            'numVacancies': len(vacancies),
            'companyName': 'Facebook'
        }

        self.assertEquals(response.status_code, 200)
        self.assertDictEqual(expectedData, response.data)



    def test_incorrectlyLargePageNumSortDateDesc(self):
        # User: Sabah
        response = self.client.get('/v1/e/vacancies/', { 'sort': 'dateDesc', 'filter': 'all', 'pageNum': 3, 'count': '10' }, **{ 'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }' })
        
        vacancySet = Vacancy.objects.filter(
                UserId__exact = 4
            ).order_by( 
                '-Created' 
            )
        vacancies = VacancySerializer(vacancySet, many=True).data

        getVacancyStats(vacancies)

        expectedData = {
            'vacancies': vacancies,
            'numPages': ceil(len(vacancies) / 10),
            'numVacancies': len(vacancies),
            'companyName': 'Facebook'
        }

        self.assertEquals(response.status_code, 200)
        self.assertDictEqual(expectedData, response.data)



    def test_onlyOpenAdvertsSortTitleAsc(self):
        # User: Sabah
        response = self.client.get('/v1/e/vacancies/', { 'sort': 'titleAsc', 'filter': 'active', 'pageNum': 1, 'count': '10' }, **{ 'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }' })
        
        vacancySet = Vacancy.objects.filter(
                UserId__exact = 4,
                IsOpen__exact = True
            ).order_by( 
                'VacancyName' 
            )
        vacancies = VacancySerializer(vacancySet, many=True).data
        vacanciesCount = Vacancy.objects.filter(UserId__exact = 4, IsOpen__exact = True).count()

        getVacancyStats(vacancies)

        expectedData = {
            'vacancies': vacancies,
            'numPages': ceil(len(vacancies) / 10),
            'numVacancies': vacanciesCount,
            'companyName': 'Facebook'
        }

        self.assertEquals(response.status_code, 200)
        self.assertDictEqual(expectedData, response.data)


    
    def test_onlyClosedSortTitleDesc(self):
        # User: Sabah
        response = self.client.get('/v1/e/vacancies/', { 'uID': 4, 'sort': 'titleDesc', 'filter': 'closed', 'pageNum': 1, 'count': '10' }, **{ 'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }' })
        
        vacancySet = Vacancy.objects.filter(
                UserId__exact = 4,
                IsOpen__exact = False
            ).order_by( 
                '-VacancyName' 
            )
        vacancies = VacancySerializer(vacancySet, many=True).data
        vacanciesCount = Vacancy.objects.filter(UserId__exact = 4, IsOpen__exact = False).count()

        getVacancyStats(vacancies)

        expectedData = {
            'vacancies': vacancies,
            'numPages': ceil(len(vacancies) / 10),
            'numVacancies': vacanciesCount,
            'companyName': 'Facebook'
        }

        self.assertEquals(response.status_code, 200)
        self.assertDictEqual(expectedData, response.data)



    def test_noVacanciesIncorrectlyLargePageNum(self):
        # User: empty
        jwt = createAccessToken(7)
        response = self.client.get('/v1/e/vacancies/', { 'sort': 'newApps', 'filter': 'all', 'pageNum': 2, 'count': '10' }, **{ 'HTTP_AUTHORIZATION': f'Bearer: { jwt }' })
        
        expectedData = {
            'vacancies': [],
            'numPages': 0,
            'numVacancies': 0,
            'companyName': 'Discord'
        }

        self.assertEquals(response.status_code, 200)
        self.assertDictEqual(expectedData, response.data)


    def test_missingParameters(self):
        # User: Sabah
        response = self.client.get('/v1/e/vacancies/', { 'sort': 'newApps' }, **{ 'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }' })

        self.assertEquals(response.status_code, 400)



    # GET STATS TESTS

    def test_validId(self):
        # Sabah
        response = self.client.get('/v1/e/vacancies/stats/', **{ 'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }' })

        expectedStats = { 
            'activeAdverts': 5, 
            'totalApplications': 24, 
            'newApplications': 13, 
            'acceptedApplications': 4, 
            'rejectedApplications': 7, 
        } 

        self.assertEquals(response.status_code, 200)
        self.assertDictEqual(expectedStats, response.data['stats'])


    def test_invalidId(self):
        jwt = createAccessToken(9999)
        response = self.client.get('/v1/e/vacancies/stats/', **{ 'HTTP_AUTHORIZATION': f'Bearer: { jwt }' })

        expectedStats = { 
            'activeAdverts': 0, 
            'totalApplications': 0, 
            'newApplications': 0, 
            'acceptedApplications': 0, 
            'rejectedApplications': 0, 
        } 
        
        self.assertEquals(response.status_code, 200)
        self.assertDictEqual(expectedStats, response.data['stats'])


    def test_noAdverts(self):
        # empty
        jwt = createAccessToken(7)
        response = self.client.get('/v1/e/vacancies/stats/', **{ 'HTTP_AUTHORIZATION': f'Bearer: { jwt }' })

        expectedStats = { 
            'activeAdverts': 0, 
            'totalApplications': 0, 
            'newApplications': 0, 
            'acceptedApplications': 0, 
            'rejectedApplications': 0, 
        } 

        self.assertEquals(response.status_code, 200)
        self.assertDictEqual(expectedStats, response.data['stats'])

    
    def test_missingAccessToken(self):
        response = self.client.get('/v1/e/vacancies/stats/')

        self.assertEquals(response.status_code, 401)


    def test_expiredJWT(self):
        jwt = createAccessToken(self.userId, 'now')
        response = self.client.get('/v1/e/vacancies/', { 'sort': 'newApps', 'filter': 'all', 'pageNum': 1, 'count': '10' }, **{ 'HTTP_AUTHORIZATION': f'Bearer: { jwt }' })

        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'Expired auth token')


    def test_invalidJWT(self):
        jwt = self.jwt[:-1]
        response = self.client.get('/v1/e/vacancies/', { 'sort': 'newApps', 'filter': 'all', 'pageNum': 1, 'count': '10' }, **{ 'HTTP_AUTHORIZATION': f'Bearer: { jwt }' })

        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'Invalid auth token')



class putIndexVacancyTests(TestCase):
    userId = 6 # Victoria
    vacancyId = 1009 # Arts development officer 
    jwt = createAccessToken(userId)

    fixtures = ['authentication/fixtures/testseed.json']


    def test_validRequest(self):
        response = self.client.put(f'/v1/e/vacancies/{ self.vacancyId }/close/', **{ 'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }' })

        self.assertEqual(response.status_code, 200)
        

    def test_unauthorisedVacancy(self):
        invalidVacancy = 1002
        response = self.client.put(f'/v1/e/vacancies/{ invalidVacancy }/close/', **{ 'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }' })

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'You do not have access to that vacancy.')


    def test_expiredJWT(self):
        jwt = createAccessToken(self.userId, 'now')
        response = self.client.put(f'/v1/e/vacancies/{ self.vacancyId }/close/', **{ 'HTTP_AUTHORIZATION': f'Bearer: { jwt }' })

        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'Expired auth token')


    def test_invalidJWT(self):
        jwt = self.jwt[:-1]
        response = self.client.put(f'/v1/e/vacancies/{ self.vacancyId }/close/', **{ 'HTTP_AUTHORIZATION': f'Bearer: { jwt }' })

        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'Invalid auth token')



class deleteIndexVacancyTests(TestCase):
    userId = 6 # Victoria
    vacancyId = 1009 # Arts development officer
    jwt = createAccessToken(userId)

    fixtures = ['authentication/fixtures/testseed.json']


    def test_validRequest(self):
        response = self.client.delete(f'/v1/e/vacancies/{ self.vacancyId }/', **{ 'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }' })

        self.assertEqual(response.status_code, 200)


    def test_unauthorisedVacancy(self):
        invalidVacancy = 1002
        response = self.client.delete(f'/v1/e/vacancies/{ invalidVacancy }/', **{ 'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }' })

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'You do not have access to that vacancy.')


    def test_expiredJWT(self):
        jwt = createAccessToken(self.userId, 'now')
        response = self.client.delete(f'/v1/e/vacancies/{ self.vacancyId }/', **{ 'HTTP_AUTHORIZATION': f'Bearer: { jwt }' })

        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'Expired auth token')


    def test_invalidJWT(self):
        jwt = self.jwt[:-1]
        response = self.client.delete(f'/v1/e/vacancies/{ self.vacancyId }/', **{ 'HTTP_AUTHORIZATION': f'Bearer: { jwt }' })

        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'Invalid auth token')