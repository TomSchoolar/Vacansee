from ast import Or
import environ
import jwt as jwtLib
from django.test import TestCase
from authentication import jwt as jwtHelper
from datetime import datetime, timezone, timedelta
from employer.models import Vacancy


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
    jwt = createJwt(1019)

    def test_getApplications(self):
        response = self.client.get('/vacancy/', { 'uID':1019, 'sort':'titleAsc', 'count':5, 'pageNum':1, 'filter':'all' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        vacancySet = Vacancy.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual((response.data['numVacancies']), len(vacancySet))