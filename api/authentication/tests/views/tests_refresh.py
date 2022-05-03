import environ
import jwt as jwtLib
from time import sleep
from django.test import TestCase
from authentication.models import RefreshToken

env = environ.Env()

class refreshTestCase(TestCase):

    userId = 2 # Adam
    password = 'password'
    email = 'ajb042@student.bham.ac.uk'

    fixtures = ['authentication/fixtures/fixtures.json']


    def setUp(self):
        # login
        loginResponse = self.client.post('/v1/login/', { 'email': self.email, 'password': self.password })
        self.assertEquals(loginResponse.status_code, 200)
        
        self.accessToken = loginResponse.data['accessToken']
        self.refreshToken = loginResponse.data['refreshToken']

        numTokens = RefreshToken.objects.all().count()
        self.assertEquals(numTokens, 1)

        # very short pause to make new jwts different
        sleep(2)

    

    def tearDown(self):
        # logout
        logoutResponse = self.client.post('/v1/logout/', **{ 'HTTP_AUTHORIZATION': f'Bearer: { self.refreshToken }' })
        self.assertEquals(logoutResponse.status_code, 200)

        numTokens = RefreshToken.objects.all().count()
        self.assertEquals(numTokens, 0)



    def test_validRefresh(self):
        # valid refresh request
        refreshResponse = self.client.post('/v1/refreshtoken/', **{ 'HTTP_AUTHORIZATION': f'Bearer: { self.refreshToken }' })
        self.assertEquals(refreshResponse.status_code, 200)

        accessToken = refreshResponse.data['accessToken']
        refreshToken = refreshResponse.data['refreshToken']

        jwtLib.decode(accessToken, env('JWT_SECRET'), algorithms=['HS256'], verify=True)
        jwtLib.decode(refreshToken, env('JWT_SECRET'), algorithms=['HS256'], verify=True)

        # get refresh family id
        familyId = RefreshToken.objects.get(Token__exact = refreshToken).FamilyId

        numTokens = RefreshToken.objects.filter(FamilyId__exact = familyId).count()
        self.assertEquals(numTokens, 2)

    

    def test_useAccessToken(self):
        # pass access token as auth token in refresh request
        refreshResponse = self.client.post('/v1/refreshtoken/', **{ 'HTTP_AUTHORIZATION': f'Bearer: { self.accessToken }' })
        self.assertEquals(refreshResponse.status_code, 401)
        self.assertEquals(refreshResponse.data['message'], 'provided refresh token is invalid')



    def test_tokenReuse(self):
        # use same token for refresh twice to check token reuse detection
        refreshResponse = self.client.post('/v1/refreshtoken/', **{ 'HTTP_AUTHORIZATION': f'Bearer: { self.refreshToken }' })
        self.assertEquals(refreshResponse.status_code, 200)

        accessToken = refreshResponse.data['accessToken']
        refreshToken = refreshResponse.data['refreshToken']

        jwtLib.decode(accessToken, env('JWT_SECRET'), algorithms=['HS256'], verify=True)
        jwtLib.decode(refreshToken, env('JWT_SECRET'), algorithms=['HS256'], verify=True)

        # get refresh family id
        familyId = RefreshToken.objects.get(Token__exact = refreshToken).FamilyId

        numTokens = RefreshToken.objects.filter(FamilyId__exact = familyId).count()
        self.assertEquals(numTokens, 2)

        # make second request
        secondRefreshResponse = self.client.post('/v1/refreshtoken/', **{ 'HTTP_AUTHORIZATION': f'Bearer: { self.refreshToken }' })
        self.assertEquals(secondRefreshResponse.status_code, 403)
        self.assertEquals(secondRefreshResponse.data['message'], 'Token reuse detected')

        numTokens = RefreshToken.objects.filter(FamilyId__exact = familyId).count()
        self.assertEquals(numTokens, 0)

    

    def test_invalidToken(self):
        refreshToken = 'potato123'
        refreshResponse = self.client.post('/v1/refreshtoken/', **{ 'HTTP_AUTHORIZATION': f'Bearer: { refreshToken }' })
        self.assertEquals(refreshResponse.status_code, 401)
        self.assertEquals(refreshResponse.data['message'], 'Invalid auth token')