import environ
import jwt as jwtLib
from django.test import TestCase
from authentication import jwt as jwtHelper
from datetime import datetime, timezone, timedelta
from employee.models import Favourite, Application, Reject


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


class decisionTestCase(TestCase):

    fixtures = ['authentication/fixtures/testseed.json']
    jwt = createJwt(2)

    def test_favouriting(self):

        userid = 1
        vacancyid = 1

        response = self.client.post('/vacancy/fav/', { "VacancyId": vacancyid }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        favouriteSet = Favourite.objects.filter(
            UserId__exact = userid,
            VacancyId__exact = vacancyid
        )

        self.assertEqual(response.status_code, 201)

        correct_response = True

        self.assertEqual(correct_response, True)

    def test_apply(self):

        userid = 1
        vacancyid = 1

        response = self.client.post('/vacancy/apply/', { "VacancyId": vacancyid }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        applicaionSet = Application.objects.filter(
            UserId__exact = userid,
            VacancyId__exact = vacancyid
        )

        self.assertEqual(response.status_code, 201)

        correct_response = True


        self.assertEqual(correct_response, True)

    def test_reject(self):

        userid = 1
        vacancyid = 1

        response = self.client.post('/vacancy/reject/', { "VacancyId": vacancyid }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        rejectSet = Reject.objects.filter(
            UserId__exact = userid,
            VacancyId__exact = vacancyid
        )

        self.assertEqual(response.status_code, 201)

        correct_response = True


        self.assertEqual(correct_response, True)
