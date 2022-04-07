from django.test import TestCase
from employee.models import Application
from authentication.tests import jwtFuncs


class applicationTestCase(TestCase):

    jwt = jwtFuncs.createJwt(1000)
    fixtures = ['authentication/fixtures/testseed.json']

    def test_delete(self):
        userId = 1000
        vacancyId = 3
        applicationId = 1011

        originalSet = Application.objects.filter(
            VacancyId__exact = vacancyId
        ).count()

        response = self.client.delete(f'/applications/delete/{ applicationId }/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        newSet = Application.objects.filter(
            VacancyId__exact = vacancyId
        )

        self.assertEqual(response.status_code, 200)


        self.assertEqual(originalSet - 1, len(newSet))


    def test_delete_invalid(self):
        response = self.client.delete('/applications/delete/10000/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 401)
