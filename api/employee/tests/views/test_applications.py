from ast import Or
import environ
import jwt as jwtLib
from django.test import TestCase
from authentication import jwt as jwtHelper
from datetime import datetime, timezone, timedelta
from employee.models import Application
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
    jwt = createJwt(1019)

    def test_delete(self):

        OriginalSet = Application.objects.filter(
            VacancyId__exact = 1
        )

        for ob in OriginalSet:
            print(ob)

        response = self.client.delete('/applications/delete/1000/', { "ApplicationId":1000 }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        NewSet = Application.objects.filter(
            VacancyId__exact = 1
        )

        for item in NewSet:
            print(item)

        self.assertEqual(response.status_code, 400)

        print(len(OriginalSet))
        print(len(NewSet))

        self.assertEqual(len(OriginalSet) - 1, len(NewSet))