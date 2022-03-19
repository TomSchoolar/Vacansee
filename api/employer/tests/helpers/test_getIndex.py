from django.test import TestCase
from employer.models import Vacancy
from employer.serializers import VacancySerializer
from employer.helpers.getIndex import getStats, getVacancyStats


class getStatsTestCase(TestCase):

    fixtures = ['authentication/fixtures/fixtures.json']
    # uses smallest seed: fixtures.json

    def test_validId(self):
        # Sabah
        uid = 4

        expectedStats = { 
            'activeAdverts': 1, 
            'totalApplications': 2, 
            'newApplications': 1, 
            'acceptedApplications': 0, 
            'rejectedApplications': 1, 
        } 

        stats = getStats(uid)

        self.assertDictEqual(expectedStats, stats)


    def test_invalidId(self):
        uid = 9999

        expectedStats = { 
            'activeAdverts': 0, 
            'totalApplications': 0, 
            'newApplications': 0, 
            'acceptedApplications': 0, 
            'rejectedApplications': 0, 
        } 

        stats = getStats(uid)

        self.assertDictEqual(expectedStats, stats)


    def test_noAdverts(self):
        # Victoria
        uid = 6

        expectedStats = { 
            'activeAdverts': 0, 
            'totalApplications': 0, 
            'newApplications': 0, 
            'acceptedApplications': 0, 
            'rejectedApplications': 0, 
        } 

        stats = getStats(uid)

        self.assertDictEqual(expectedStats, stats)



class getVacancyStatsTestCase(TestCase):

    fixtures = ['authentication/fixtures/testseed.json']
    # uses expanded testseed.json

    def test_emptyList(self):
        emptyList = []
        getVacancyStats(emptyList)
        self.assertListEqual([], emptyList)


    def test_singletonList(self):
        # Junior Developer Vacancy
        vacancySet = Vacancy.objects.get(pk = 1)
        vacancy = [VacancySerializer(vacancySet).data]
        
        getVacancyStats(vacancy)

        vacancy = vacancy[0]

        self.assertEquals(vacancy['NewApplications'], 4)
        self.assertEquals(vacancy['AcceptedApplications'], 1)
        self.assertEquals(vacancy['RejectedApplications'], 1)


    def test_list(self):
        # Sabah
        vacancySet = Vacancy.objects.filter(UserId__exact = 4)
        vacancies = VacancySerializer(vacancySet, many=True).data
        
        getVacancyStats(vacancies)

        expectedStats = {
            1: { 'new': 4, 'accepted': 1, 'rejected': 1 },     # junior developer
            2: { 'new': 3, 'accepted': 0, 'rejected': 3 },     # senior developer
            1000: { 'new': 1, 'accepted': 4, 'rejected': 0 },  # architect
            1001: { 'new': 0, 'accepted': 1, 'rejected': 4 }   # structural engineer
        }

        for vacancy in vacancies:
            stats = expectedStats[vacancy['VacancyId']]
            self.assertEquals(vacancy['NewApplications'], stats['new'])
            self.assertEquals(vacancy['AcceptedApplications'], stats['accepted'])
            self.assertEquals(vacancy['RejectedApplications'], stats['rejected'])
