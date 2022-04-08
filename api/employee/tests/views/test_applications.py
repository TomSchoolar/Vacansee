import environ
import jwt as jwtLib
from django.test import TestCase
from employee.models import Application
from authentication import jwt as jwtHelper
from datetime import datetime, timezone, timedelta
from employee.serializers import ApplicationSerializer


env = environ.Env()


def createJwt(uid, expire='later'):
    jwt = { 
        'id': uid,
        'exp': datetime.now(tz=timezone.utc) + timedelta(minutes=60),
        'iat': datetime.now(tz=timezone.utc)
    }

    if expire == 'now':
        jwt['exp'] = datetime.now(tz=timezone.utc) - timedelta(minutes=1)

    encodedJWT = jwtLib.encode(
        jwt,
        env('JWT_SECRET'),
        algorithm='HS256'
    )

    return encodedJWT


class applicationTestCase(TestCase):

    fixtures = ['authentication/fixtures/testseed.json']
    jwt = createJwt(1000)

    def test_getApplications(self):
        response = self.client.get('/applications/', { 'uID':1019, 'sort':'titleAsc', 'count':5, 'pageNum':1, 'filter':'all' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        applicationSet = Application.objects.filter(
            UserId__exact = 1019
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['applications']), len(applicationSet))

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
        response = self.client.delete('/applications/delete/1019/', { "ApplicationId":1019 }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 401)
