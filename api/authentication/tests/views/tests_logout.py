from venv import create
from django.test import TestCase
from ..jwtFuncs import createRefreshToken
from authentication.models import RefreshToken


class logoutTestCase(TestCase):

    userId = 2 # Adam
    password = 'password'
    email = 'ajb042@student.bham.ac.uk'

    fixtures = ['authentication/fixtures/fixtures.json']

    def test_validLogout(self):
        loginResponse = self.client.post('/login/', { 'email': self.email, 'password': self.password })
        self.assertEquals(loginResponse.status_code, 200)
        
        refreshToken = loginResponse.data['refreshToken']

        numTokens = RefreshToken.objects.all().count()
        self.assertEquals(numTokens, 1)

        logoutResponse = self.client.post('/logout/', **{ 'HTTP_AUTHORIZATION': f'Bearer: { refreshToken }' })

        self.assertEquals(logoutResponse.status_code, 200)

        numTokens = RefreshToken.objects.all().count()
        self.assertEquals(numTokens, 0)



    def test_refreshTokenNotSaved(self):
        refreshToken = createRefreshToken(self.userId)

        numTokens = RefreshToken.objects.all().count()
        self.assertEquals(numTokens, 0)

        logoutResponse = self.client.post('/logout/', **{ 'HTTP_AUTHORIZATION': f'Bearer: { refreshToken }' })

        self.assertEquals(logoutResponse.status_code, 200)

        numTokens = RefreshToken.objects.all().count()
        self.assertEquals(numTokens, 0)


    
    def test_refreshTokenMissing(self):
        logoutResponse = self.client.post('/logout/')

        self.assertEquals(logoutResponse.status_code, 401)
        self.assertEquals(logoutResponse.data['message'], 'Missing auth token')

    

    def test_invalidRefreshToken(self):
        invalidToken = 'potato123'
        logoutResponse = self.client.post('/logout/', **{ 'HTTP_AUTHORIZATION': f'Bearer: { invalidToken }' })

        self.assertEquals(logoutResponse.status_code, 401)
        self.assertEquals(logoutResponse.data['message'], 'Invalid auth token')