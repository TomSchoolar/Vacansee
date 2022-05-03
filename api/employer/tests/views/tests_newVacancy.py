from copy import copy
from json import dumps
from django.test import TestCase
from employer.models import Vacancy
from .. import comparisonUtils as comp
from employer.serializers import VacancySerializer
from authentication.tests.jwtFuncs import createAccessToken


class newVacancyTestCase(TestCase):

    userId = 4 # Sabah
    jwt = createAccessToken(userId)
    fixtures = ['authentication/fixtures/fixtures.json']
    vacancyData = {
        'VacancyName': 'test vacancy',
        'Salary': '£35,000 pa',
        'Description': 'This is a test vacancy, I need some words to fill this field',
        'SkillsRequired': dumps(['This is a skill', 'Another skill', 'You know what, take another skill']),
        'ExperienceRequired': dumps(['Tester&&1 year', 'Life experience&&18 years', 'fuck knows what else&&1 minute']),
        'TimeZone': 0,
        'Tags': dumps([0, 1, 3, 4]),
        'PhoneNumber': '07711 264845',
        'Email': 'orange_you.glad-I@didntsay.banana',
        'Location': 'London'
    }

    # GET INDEX TESTS

    def test_validRequest(self):
        testData = copy(self.vacancyData)

        initialVacancyCount = Vacancy.objects.filter(UserId__exact = self.userId).count()        
        response = self.client.post('/v1/e/vacancies/', data=testData, content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})
        finalVacancyCount = Vacancy.objects.filter(UserId__exact = self.userId).count() 

        savedVacancySet = Vacancy.objects.get(VacancyName__exact = self.vacancyData['VacancyName'])
        savedVacancy = VacancySerializer(savedVacancySet).data

        self.assertEquals(response.status_code, 200)
        self.assertLess(initialVacancyCount, finalVacancyCount)

        comp.compareLists(self, savedVacancy['SkillsRequired'], testData['SkillsRequired'])
        del savedVacancy['SkillsRequired']
        del testData['SkillsRequired']

        comp.compareLists(self, savedVacancy['ExperienceRequired'], testData['ExperienceRequired'])
        del savedVacancy['ExperienceRequired']
        del testData['ExperienceRequired']

        comp.compareLists(self, savedVacancy['Tags'], testData['Tags'])
        del savedVacancy['Tags']
        del testData['Tags']

        comp.compareDicts(self, savedVacancy, testData)

        savedVacancySet.delete()



    def test_missingOptionalField(self):
        testData = copy(self.vacancyData)
        testData['SkillsRequired'] = []
        testData['ExperienceRequired'] = []

        initialVacancyCount = Vacancy.objects.filter(UserId__exact = self.userId).count()        
        response = self.client.post('/v1/e/vacancies/', data=testData, content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})
        finalVacancyCount = Vacancy.objects.filter(UserId__exact = self.userId).count() 

        self.assertEquals(response.status_code, 200)

        savedVacancySet = Vacancy.objects.get(VacancyName__exact = testData['VacancyName'])
        savedVacancy = VacancySerializer(savedVacancySet).data
        
        self.assertLess(initialVacancyCount, finalVacancyCount)

        comp.compareLists(self, savedVacancy['SkillsRequired'], testData['SkillsRequired'])
        del savedVacancy['SkillsRequired']
        del testData['SkillsRequired']

        comp.compareLists(self, savedVacancy['ExperienceRequired'], testData['ExperienceRequired'])
        del savedVacancy['ExperienceRequired']
        del testData['ExperienceRequired']

        comp.compareLists(self, savedVacancy['Tags'], testData['Tags'])
        del savedVacancy['Tags']
        del testData['Tags']

        comp.compareDicts(self, savedVacancy, testData)

        savedVacancySet.delete()



    def test_fieldTooLarge(self):
        testData = copy(self.vacancyData)
        testData['Tags'] = dumps([el for el in range(15)])

        initialVacancyCount = Vacancy.objects.filter(UserId__exact = self.userId).count()        
        response = self.client.post('/v1/e/vacancies/', testData, content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})
        finalVacancyCount = Vacancy.objects.filter(UserId__exact = self.userId).count() 
        
        self.assertEquals(response.status_code, 400)
        self.assertEquals(initialVacancyCount, finalVacancyCount)



    def test_missingRequiredField(self):
        testData = copy(self.vacancyData)
        del testData['VacancyName']

        initialVacancyCount = Vacancy.objects.filter(UserId__exact = self.userId).count()        
        response = self.client.post('/v1/e/vacancies/', testData, content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})
        finalVacancyCount = Vacancy.objects.filter(UserId__exact = self.userId).count() 

        self.assertEquals(response.status_code, 400)
        self.assertEquals(initialVacancyCount, finalVacancyCount)

    

    def test_missingAccessToken(self):
        initialVacancyCount = Vacancy.objects.filter(UserId__exact = self.userId).count()        
        response = self.client.post('/v1/e/vacancies/', self.vacancyData, content_type='application/json')
        finalVacancyCount = Vacancy.objects.filter(UserId__exact = self.userId).count() 
        
        self.assertEquals(response.status_code, 401)
        self.assertEquals(initialVacancyCount, finalVacancyCount)

    

