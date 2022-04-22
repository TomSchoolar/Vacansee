import json
from copy import copy
from django.test import TestCase
from employer.models import Vacancy
from employer.serializers import VacancySerializer
from authentication.tests.jwtFuncs import createAccessToken


class editVacancyTestCase(TestCase):

    userId = 4 # Sabah
    vacancyId = 1
    invalidVacancyId = 3
    jwt = createAccessToken(userId)
    fixtures = ['authentication/fixtures/fixtures.json']

    # GET INDEX TESTS

    def compareLists(self, dbList, testList):
        for i, dbSkill in enumerate(dbList):
            if type(testList) is not list:
                testSkill = json.loads(testList)[i]
            else:
                testSkill = testList[i]
            self.assertEquals(testSkill, dbSkill)



    def compareDicts(self, dbDict, testDict):
        testDict['VacancyId'] = dbDict['VacancyId']
        testDict['UserId'] = self.userId
        testDict['IsOpen'] = True
        
        del dbDict['Created']

        return self.assertDictEqual(dbDict, testDict)



    def test_validRequest(self):     
        response = self.client.get(f'/e/vacancy/edit/{ self.vacancyId }/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        savedVacancySet = Vacancy.objects.get(pk = self.vacancyId)
        savedVacancy = VacancySerializer(savedVacancySet).data

        self.assertEquals(response.status_code, 200)

        self.compareLists(savedVacancy['SkillsRequired'], savedVacancy['SkillsRequired'])
        del savedVacancy['SkillsRequired']

        self.compareLists(savedVacancy['ExperienceRequired'], savedVacancy['ExperienceRequired'])
        del savedVacancy['ExperienceRequired']

        self.compareLists(savedVacancy['Tags'], savedVacancy['Tags'])
        del savedVacancy['Tags']

        self.compareDicts(savedVacancy, savedVacancy)



    def test_invalidVacancyId(self):  
        response = self.client.get(f'/e/vacancy/edit/{ self.invalidVacancyId }/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})
        self.assertEquals(response.status_code, 401)
        self.assertEquals(response.data['message'], 'That vacancy is not available for editing.')



    def test_missingAccessToken(self):  
        response = self.client.get(f'/e/vacancy/edit/{ self.vacancyId }/')
        self.assertEquals(response.status_code, 401)

    

