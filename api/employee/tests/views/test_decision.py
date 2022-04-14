from django.test import TestCase
from authentication.tests.jwtFuncs import createAccessToken
from employee.models import Favourite, Application, Reject



class decisionTestCase(TestCase):

    userId = 1
    vacancyId = 1
    jwt = createAccessToken(userId)
    fixtures = ['authentication/fixtures/testseed.json']

    def test_favouriting(self):
        response = self.client.post('/vacancy/fav/', { "VacancyId": self.vacancyId }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 201)

    def test_apply(self):
        response = self.client.post('/vacancy/apply/', { "VacancyId": self.vacancyId }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 201)

    def test_validReject(self):
        response = self.client.post('/vacancy/reject/', { "VacancyId": self.vacancyId }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 201)

    def test_invalidReject(self):
        response = self.client.post('/vacancy/reject/', { "VacancyId": 9999 }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], 'That vacancy is not open for applications')

    def test_missingParameters(self):
        response = self.client.post('/vacancy/reject/', { }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 400)

    def test_expiredJWT(self):
        jwt = createAccessToken(self.jwt, 'now')

        response = self.client.post('/vacancy/reject/', { "VacancyId": self.vacancyId }, **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Expired auth token')

    def test_invalidJWT(self):
        jwt = self.jwt[:-1]

        response = self.client.post('/vacancy/reject/', { "VacancyId": self.vacancyId }, **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Invalid auth token')