from copy import copy
from json import dumps
from django.test import TestCase
from employer.models import Vacancy
from .. import comparisonUtils as comp
from employer.serializers import VacancySerializer
from authentication.tests.jwtFuncs import createAccessToken


class editVacancyGetTestCase(TestCase):

    userId = 4 # Sabah
    vacancyId = 1
    invalidVacancyId = 3
    jwt = createAccessToken(userId)
    fixtures = ['authentication/fixtures/fixtures.json']

    # GET INDEX TESTS

    def test_validRequest(self):     
        response = self.client.get(f'/v1/e/vacancies/{ self.vacancyId }/edit/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        savedVacancySet = Vacancy.objects.get(pk = self.vacancyId)
        savedVacancy = VacancySerializer(savedVacancySet).data

        self.assertEquals(response.status_code, 200)

        comp.compareLists(self, savedVacancy['SkillsRequired'], savedVacancy['SkillsRequired'])
        del savedVacancy['SkillsRequired']

        comp.compareLists(self, savedVacancy['ExperienceRequired'], savedVacancy['ExperienceRequired'])
        del savedVacancy['ExperienceRequired']

        comp.compareLists(self, savedVacancy['Tags'], savedVacancy['Tags'])
        del savedVacancy['Tags']

        comp.compareDicts(self, savedVacancy, savedVacancy)



    def test_invalidVacancyId(self):  
        response = self.client.get(f'/v1/e/vacancies/{ self.invalidVacancyId }/edit/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})
        self.assertEquals(response.status_code, 401)
        self.assertEquals(response.data['message'], 'That vacancy is not available for editing.')



    def test_missingAccessToken(self):  
        response = self.client.get(f'/v1/e/vacancies/{ self.vacancyId }/edit/')
        self.assertEquals(response.status_code, 401)

    


class editVacancyPutTestCase(TestCase):

    userId = 4 # Sabah
    vacancyId = 1
    invalidVacancyId = 3
    jwt = createAccessToken(userId)
    fixtures = ['authentication/fixtures/fixtures.json']

    # GET INDEX TESTS

    def test_validRequest(self):
        savedVacancySet = Vacancy.objects.get(pk = self.vacancyId)
        savedVacancy = VacancySerializer(savedVacancySet).data

        savedVacancy['Description'] = 'Looking for a graduate developer with a foundation in Python'
        savedVacancy['Salary'] = '£30,000 pa'

        modifiedVacancy = copy(savedVacancy)

        del modifiedVacancy['IsOpen']
        del modifiedVacancy['UserId']
        del modifiedVacancy['VacancyId']
        
        modifiedVacancy['SkillsRequired'] = dumps(modifiedVacancy['SkillsRequired'])        
        modifiedVacancy['ExperienceRequired'] = dumps(modifiedVacancy['ExperienceRequired'])
        modifiedVacancy['Tags'] = dumps(modifiedVacancy['Tags'])

        response = self.client.put(f'/v1/e/vacancies/{ self.vacancyId }/', modifiedVacancy, content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEquals(response.status_code, 200)

        updatedVacancySet = Vacancy.objects.get(pk = self.vacancyId)
        updatedVacancy = VacancySerializer(updatedVacancySet).data

        self.assertDictEqual(savedVacancy, updatedVacancy)

    

    def test_tooManySkills(self):
        savedVacancySet = Vacancy.objects.get(pk = self.vacancyId)
        savedVacancy = VacancySerializer(savedVacancySet).data

        modifiedVacancy = copy(savedVacancy)

        del modifiedVacancy['IsOpen']
        del modifiedVacancy['UserId']
        del modifiedVacancy['VacancyId']

        modifiedVacancy['SkillsRequired'].append('So many skills!')
        
        modifiedVacancy['SkillsRequired'] = dumps(modifiedVacancy['SkillsRequired'])        
        modifiedVacancy['ExperienceRequired'] = dumps(modifiedVacancy['ExperienceRequired'])
        modifiedVacancy['Tags'] = dumps(modifiedVacancy['Tags'])

        response = self.client.put(f'/v1/e/vacancies/{ self.vacancyId }/', modifiedVacancy, content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.data['message'], 'Invalid vacancy data: <ul class="errorlist"><li>SkillsRequired<ul class="errorlist"><li>List contains 4 items, it should contain no more than 3.</li></ul></li></ul>')

        updatedVacancySet = Vacancy.objects.get(pk = self.vacancyId)
        updatedVacancy = VacancySerializer(updatedVacancySet).data

        savedVacancy['SkillsRequired'].pop()

        self.assertDictEqual(savedVacancy, updatedVacancy)