import environ
import jwt as jwtLib
from django.test import TestCase
from authentication.models import RefreshToken

env = environ.Env()

class LoginPostTestClass(TestCase):

    password = 'password'
    email = 'ajb042@student.bham.ac.uk'

    fixtures = ['authentication/fixtures/fixtures.json']


    def tearDown(self):
        RefreshToken.objects.all().delete()


    def test_validLoginRequest(self):

        response = self.client.post('/login/', { 'email': self.email, 'password': self.password })
        
        expectedUserData = {
            'IsEmployer': False,
            'Email': self.email
        }

        self.assertDictEqual(response.data['userData'], expectedUserData)

        accessToken = jwtLib.decode(response.data['accessToken'], env('JWT_SECRET'), algorithms=['HS256'], verify=True)
        refreshToken = jwtLib.decode(response.data['refreshToken'], env('JWT_SECRET'), algorithms=['HS256'], verify=True)

        
        self.assertTrue('exp' in accessToken)
        self.assertTrue('iat' in accessToken)
        self.assertEquals(accessToken['id'], 2)
        self.assertEquals(accessToken['typ'], 'access')

        self.assertTrue('exp' in refreshToken)
        self.assertTrue('iat' in refreshToken)
        self.assertEquals(refreshToken['id'], 2)
        self.assertEquals(refreshToken['typ'], 'refresh')

        RefreshToken.objects.get(Token__exact = response.data['refreshToken'])


    def test_incorrectEmail(self):
        response = self.client.post('/login/', { 'email': 'gxvy123@student.bham.ac.uk', 'password': self.password })

        self.assertEquals(response.status_code, 401)

    
    def test_incorrectPassword(self):
        response = self.client.post('/login/', { 'email': self.email, 'password': 'potato' })

        self.assertEquals(response.status_code, 401)
    

    def test_missingParameters(self):
        response = self.client.post('/login/')

        self.assertEquals(response.status_code, 400)
    

    def test_loginTwoAccountsCheckRefreshFamily(self):
        # login to two accounts consecutively and make sure the refresh token records have different, and correct family ids
        secondEmail = 'sxd110@student.bham.ac.uk'

        firstResponse = self.client.post('/login/', { 'email': self.email, 'password': self.password })
        
        firstRefreshToken = firstResponse.data['refreshToken']
        firstTokenFamily = RefreshToken.objects.get(Token__exact = firstRefreshToken).FamilyId

        self.assertEquals(firstTokenFamily, 0)

        secondResponse = self.client.post('/login/', { 'email': secondEmail, 'password': self.password })
        
        secondRefreshToken = secondResponse.data['refreshToken']
        secondTokenFamily = RefreshToken.objects.get(Token__exact = secondRefreshToken).FamilyId

        self.assertEquals(secondTokenFamily, 1)
