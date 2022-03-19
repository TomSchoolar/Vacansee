from django.test import TestCase
from employer.helpers.getIndex import getStats

class getStatsTestCase(TestCase):

    fixtures = ['authentication/fixtures/fixtures.json']

    def test_validId(self):
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