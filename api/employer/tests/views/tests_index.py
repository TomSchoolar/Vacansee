from math import ceil
from django.test import TestCase
from django.core import management
from employer.models import Vacancy
from django.db.models import Count, Q
from employer.serializers import VacancySerializer
from employer.helpers.getIndex import getVacancyStats


class indexTestCase(TestCase):

    fixtures = ['authentication/fixtures/testseed.json']

    # GET INDEX TESTS

    def test_validRequestSortNewApplications(self):
        # User: Sabah
        response = self.client.get('/e/vacancy/', { 'uID': 4, 'sort': 'newApps', 'filter': 'all', 'pageNum': 1, 'count': '10' })
        
        vacancySet = Vacancy.objects.filter(
                UserId__exact = 4
            ).annotate( 
                applicationCount = Count('application', filter=Q(application__ApplicationStatus__exact='PENDING')) 
            ).order_by( 
                '-applicationCount' 
            )
        vacancies = VacancySerializer(vacancySet, many=True).data

        getVacancyStats(vacancies)

        expectedData = {
            'vacancies': vacancies,
            'numPages': ceil(len(vacancies) / 10),
            'numVacancies': len(vacancies),
            'companyName': 'Facebook'
        }

        self.assertDictEqual(expectedData, response.data)


    def test_incorrectlyLargePageNumSortDateDesc(self):
        # User: Sabah
        response = self.client.get('/e/vacancy/', { 'uID': 4, 'sort': 'dateDesc', 'filter': 'all', 'pageNum': 3, 'count': '10' })
        
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

        self.assertDictEqual(expectedData, response.data)



    def test_onlyOpenAdvertsSortTitleAsc(self):
        # User: Sabah
        response = self.client.get('/e/vacancy/', { 'uID': 4, 'sort': 'titleAsc', 'filter': 'active', 'pageNum': 1, 'count': '10' })
        
        vacancySet = Vacancy.objects.filter(
                UserId__exact = 4,
                IsOpen__exact = True
            ).order_by( 
                'VacancyName' 
            )
        vacancies = VacancySerializer(vacancySet, many=True).data

        getVacancyStats(vacancies)

        expectedData = {
            'vacancies': vacancies,
            'numPages': ceil(len(vacancies) / 10),
            'numVacancies': len(vacancies),
            'companyName': 'Facebook'
        }

        self.assertDictEqual(expectedData, response.data)

    
    def test_onlyClosedSortTitleDesc(self):
        # User: Sabah
        response = self.client.get('/e/vacancy/', { 'uID': 4, 'sort': 'titleDesc', 'filter': 'closed', 'pageNum': 1, 'count': '10' })
        
        vacancySet = Vacancy.objects.filter(
                UserId__exact = 4,
                IsOpen__exact = False
            ).order_by( 
                '-VacancyName' 
            )
        vacancies = VacancySerializer(vacancySet, many=True).data

        getVacancyStats(vacancies)

        expectedData = {
            'vacancies': vacancies,
            'numPages': ceil(len(vacancies) / 10),
            'numVacancies': len(vacancies),
            'companyName': 'Facebook'
        }

        self.assertDictEqual(expectedData, response.data)


    def test_noVacanciesIncorrectlyLargePageNum(self):
        # User: Victoria
        response = self.client.get('/e/vacancy/', { 'uID': 6, 'sort': 'newApps', 'filter': 'all', 'pageNum': 2, 'count': '10' })
        
        expectedData = {
            'vacancies': [],
            'numPages': 0,
            'numVacancies': 0,
            'companyName': 'Facebook'
        }

        self.assertDictEqual(expectedData, response.data)

    
    def test_missingParameters(self):
        # User: Sabah
        response = self.client.get('/e/vacancy/', { 'uID': 4, 'sort': 'newApps' })

        self.assertEquals(response.status_code, 400)


    # GET STATS TESTS

    def test_validId(self):
        # Sabah
        response = self.client.get('/e/vacancy/stats/', { 'uID': 4 })

        expectedStats = { 
            'activeAdverts': 6, 
            'totalApplications': 28, 
            'newApplications': 15, 
            'acceptedApplications': 5, 
            'rejectedApplications': 8, 
        } 

        self.assertDictEqual(expectedStats, response.data['stats'])


    def test_invalidId(self):
        response = self.client.get('/e/vacancy/stats/', { 'uID': 9999 })

        expectedStats = { 
            'activeAdverts': 0, 
            'totalApplications': 0, 
            'newApplications': 0, 
            'acceptedApplications': 0, 
            'rejectedApplications': 0, 
        } 

        self.assertDictEqual(expectedStats, response.data['stats'])


    def test_noAdverts(self):
        # Victoria
        response = self.client.get('/e/vacancy/stats/', { 'uID': 6 })

        expectedStats = { 
            'activeAdverts': 0, 
            'totalApplications': 0, 
            'newApplications': 0, 
            'acceptedApplications': 0, 
            'rejectedApplications': 0, 
        } 

        self.assertDictEqual(expectedStats, response.data['stats'])

    
    def test_missingParameter(self):
        # Sabah
        response = self.client.get('/e/vacancy/stats/')

        self.assertEquals(response.status_code, 400)