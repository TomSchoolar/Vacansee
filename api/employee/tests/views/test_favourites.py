import environ
import jwt as jwtLib
from django.test import TestCase
from authentication.helpers import jwt as jwtHelper
from datetime import datetime, timezone, timedelta
from employee.models import Favourite


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


class favouritesTestCase(TestCase):

    fixtures = ['authentication/fixtures/testseed.json']
    jwt = createJwt(2)

    def test_getFavourites(self):
        response = self.client.get('/favourites/', { 'uID':2, 'sort':'titleAsc', 'count':5, 'pageNum':1 }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        favouriteSet = Favourite.objects.filter(
            UserId__exact = 2
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['numVacancies'], len(favouriteSet))