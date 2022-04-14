from copy import copy
from django.test import TestCase
from employer.models import Vacancy
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
        'SkillsRequired': ['This is a skill', 'Another skill', 'You know what, take another skill'],
        'ExperienceRequired': ['Tester¬1 year', 'Life experience¬18 years', 'fuck knows what else¬1 minute'],
        'TimeZone': 0,
        'Tags': [0,1,3,4],
        'PhoneNumber': '07711 264845',
        'Email': 'orange_you.glad-I@didntsay.banana',
        'Location': 'London'
    }

    # GET INDEX TESTS

    def test_validRequest(self):
        initialVacancyCount = Vacancy.objects.filter(UserId__exact = self.userId).count()        
        response = self.client.post('/e/vacancy/', self.vacancyData, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})
        finalVacancyCount = Vacancy.objects.filter(UserId__exact = self.userId).count() 

        savedVacancySet = Vacancy.objects.filter(VacancyName__exact = self.vacancyData['VacancyName'])
        savedVacancy = VacancySerializer(savedVacancySet).data

        self.assertEquals(response.status_code, 200)
        self.assertLess(initialVacancyCount, finalVacancyCount)
        self.assertDictEqual(savedVacancy, self.vacancyData)

        savedVacancySet.delete()



    def test_missingOptionalField(self):
        testData = copy(self.vacancyData)
        testData['SkillsRequired'] = []
        testData['ExperienceRequired'] = []

        initialVacancyCount = Vacancy.objects.filter(UserId__exact = self.userId).count()        
        response = self.client.post('/e/vacancy/', testData, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})
        finalVacancyCount = Vacancy.objects.filter(UserId__exact = self.userId).count() 

        savedVacancySet = Vacancy.objects.filter(VacancyName__exact = self.vacancyData['VacancyName'])
        savedVacancy = VacancySerializer(savedVacancySet).data

        self.assertEquals(response.status_code, 200)
        self.assertLess(initialVacancyCount, finalVacancyCount)
        self.assertDictEqual(savedVacancy, testData)

        savedVacancySet.delete()



    def test_fieldTooLarge(self):
        testData = copy(self.vacancyData)
        testData['Tags'] = [el for el in range(15)]

        initialVacancyCount = Vacancy.objects.filter(UserId__exact = self.userId).count()        
        response = self.client.post('/e/vacancy/', testData)
        finalVacancyCount = Vacancy.objects.filter(UserId__exact = self.userId).count() 
        
        self.assertEquals(response.status_code, 400)
        self.assertEquals(initialVacancyCount, finalVacancyCount)



    def test_missingRequiredField(self):
        testData = copy(self.vacancyData)
        del testData['VacancyName']

        initialVacancyCount = Vacancy.objects.filter(UserId__exact = self.userId).count()        
        response = self.client.post('/e/vacancy/', testData)
        finalVacancyCount = Vacancy.objects.filter(UserId__exact = self.userId).count() 
        
        self.assertEquals(response.status_code, 400)
        self.assertEquals(initialVacancyCount, finalVacancyCount)

    

    def test_missingAccessToken(self):
        initialVacancyCount = Vacancy.objects.filter(UserId__exact = self.userId).count()        
        response = self.client.post('/e/vacancy/', self.vacancyData)
        finalVacancyCount = Vacancy.objects.filter(UserId__exact = self.userId).count() 
        
        self.assertEquals(response.status_code, 401)
        self.assertEquals(initialVacancyCount, finalVacancyCount)

    

