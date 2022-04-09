from django.test import TestCase
from employee.models import Favourite
from authentication.tests.jwtFuncs import createAccessToken



class favouritesTestCase(TestCase):

    fixtures = ['authentication/fixtures/testseed.json']
    jwt = createAccessToken(2)

    def test_getFavourites(self):
        response = self.client.get('/favourites/', { 'uID':2, 'sort':'titleAsc', 'count':5, 'pageNum':1 }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        favouriteSet = Favourite.objects.filter(
            UserId__exact = 2
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['numVacancies'], len(favouriteSet))