import json
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
        'SkillsRequired': json.dumps(['This is a skill', 'Another skill', 'You know what, take another skill']),
        'ExperienceRequired': json.dumps(['Tester&&1 year', 'Life experience&&18 years', 'fuck knows what else&&1 minute']),
        'TimeZone': 0,
        'Tags': json.dumps([0, 1, 3, 4]),
        'PhoneNumber': '07711 264845',
        'Email': 'orange_you.glad-I@didntsay.banana',
        'Location': 'London'
    }

    # GET INDEX TESTS

    def compareLists(self, dbList, testList):
        for i, dbSkill in enumerate(dbList):
            testSkill = json.loads(testList)[i]
            self.assertEquals(testSkill, dbSkill)



    def compareDicts(self, dbDict, testDict):
        testDict['VacancyId'] = dbDict['VacancyId']
        testDict['UserId'] = self.userId
        testDict['IsOpen'] = True
        
        del dbDict['Created']

        return self.assertDictEqual(dbDict, testDict)



    def test_validRequest(self):
        testData = copy(self.vacancyData)

        initialVacancyCount = Vacancy.objects.filter(UserId__exact = self.userId).count()        
        response = self.client.post('/e/vacancy/', data=testData, content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})
        finalVacancyCount = Vacancy.objects.filter(UserId__exact = self.userId).count() 

        savedVacancySet = Vacancy.objects.get(VacancyName__exact = self.vacancyData['VacancyName'])
        savedVacancy = VacancySerializer(savedVacancySet).data


        self.maxDiff = None
        self.assertEquals(response.status_code, 200)
        self.assertLess(initialVacancyCount, finalVacancyCount)

        self.compareLists(savedVacancy['SkillsRequired'], testData['SkillsRequired'])
        del savedVacancy['SkillsRequired']
        del testData['SkillsRequired']

        self.compareLists(savedVacancy['ExperienceRequired'], testData['ExperienceRequired'])
        del savedVacancy['ExperienceRequired']
        del testData['ExperienceRequired']

        self.compareLists(savedVacancy['Tags'], testData['Tags'])
        del savedVacancy['Tags']
        del testData['Tags']

        self.compareDicts(savedVacancy, testData)

        savedVacancySet.delete()



    def test_missingOptionalField(self):
        testData = copy(self.vacancyData)
        testData['SkillsRequired'] = []
        testData['ExperienceRequired'] = []

        initialVacancyCount = Vacancy.objects.filter(UserId__exact = self.userId).count()        
        response = self.client.post('/e/vacancy/', data=testData, content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})
        finalVacancyCount = Vacancy.objects.filter(UserId__exact = self.userId).count() 

        self.assertEquals(response.status_code, 200)

        savedVacancySet = Vacancy.objects.get(VacancyName__exact = testData['VacancyName'])
        savedVacancy = VacancySerializer(savedVacancySet).data
        
        self.assertLess(initialVacancyCount, finalVacancyCount)

        self.compareLists(savedVacancy['SkillsRequired'], testData['SkillsRequired'])
        del savedVacancy['SkillsRequired']
        del testData['SkillsRequired']

        self.compareLists(savedVacancy['ExperienceRequired'], testData['ExperienceRequired'])
        del savedVacancy['ExperienceRequired']
        del testData['ExperienceRequired']

        self.compareLists(savedVacancy['Tags'], testData['Tags'])
        del savedVacancy['Tags']
        del testData['Tags']

        self.compareDicts(savedVacancy, testData)

        savedVacancySet.delete()



    def test_fieldTooLarge(self):
        testData = copy(self.vacancyData)
        testData['Tags'] = json.dumps([el for el in range(15)])

        initialVacancyCount = Vacancy.objects.filter(UserId__exact = self.userId).count()        
        response = self.client.post('/e/vacancy/', testData, content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})
        finalVacancyCount = Vacancy.objects.filter(UserId__exact = self.userId).count() 
        
        self.assertEquals(response.status_code, 400)
        self.assertEquals(initialVacancyCount, finalVacancyCount)



    def test_missingRequiredField(self):
        testData = copy(self.vacancyData)
        del testData['VacancyName']

        initialVacancyCount = Vacancy.objects.filter(UserId__exact = self.userId).count()        
        response = self.client.post('/e/vacancy/', testData, content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})
        finalVacancyCount = Vacancy.objects.filter(UserId__exact = self.userId).count() 

        self.assertEquals(response.status_code, 400)
        self.assertEquals(initialVacancyCount, finalVacancyCount)

    

    def test_missingAccessToken(self):
        initialVacancyCount = Vacancy.objects.filter(UserId__exact = self.userId).count()        
        response = self.client.post('/e/vacancy/', self.vacancyData, content_type='application/json')
        finalVacancyCount = Vacancy.objects.filter(UserId__exact = self.userId).count() 
        
        self.assertEquals(response.status_code, 401)
        self.assertEquals(initialVacancyCount, finalVacancyCount)

    

