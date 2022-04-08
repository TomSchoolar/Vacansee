import environ
import jwt as jwtLib
from django.test import TestCase
from employee.models import Application
from datetime import datetime, timezone, timedelta


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

    userId = 2 # Adam
    vacancyId = 1
    jwt = createJwt(userId)
    applicationId = 1003
    fixtures = ['authentication/fixtures/testseed.json']

    def test_getApplications(self):
        response = self.client.get('/applications/', { 'sort': 'titleAsc', 'count': 100, 'pageNum': 1, 'filter': 'all' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        applicationSet = Application.objects.filter(
            UserId__exact = self.userId
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['applications']), len(applicationSet))



    def test_getApplicationsStats(self):
        response = self.client.get('/applications/stats/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        numApps = Application.objects.filter(
            UserId__exact = self.userId
        ).count()

        self.assertEquals(response.status_code, 200)
        self.assertEqual(response.data['total'], numApps)



    def test_getApplicationsDetails(self):
        response = self.client.get(f'/applications/{ self.applicationId }/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 200)



    def test_delete(self):

        originalSet = Application.objects.filter(
            VacancyId__exact = self.vacancyId
        ).count()

        response = self.client.delete(f'/applications/delete/{ self.applicationId }/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        newSet = Application.objects.filter(
            VacancyId__exact = self.vacancyId
        ).count()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(originalSet - 1, newSet)



    def test_delete_invalid(self):
        applicationId = 1019
        response = self.client.delete(f'/applications/delete/{ applicationId }/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 401)
