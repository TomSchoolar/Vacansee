from django.test import TestCase
from employer.models import Vacancy
from authentication.tests.jwtFuncs import createJwt



class applicationTestCase(TestCase):

    fixtures = ['authentication/fixtures/testseed.json']
    jwt = createJwt(1019)

    def test_getApplications(self):
        response = self.client.get('/vacancy/', { 'uID':1019, 'sort':'titleAsc', 'count':5, 'pageNum':1, 'filter':'all' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        vacancySet = Vacancy.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual((response.data['numVacancies']), len(vacancySet))