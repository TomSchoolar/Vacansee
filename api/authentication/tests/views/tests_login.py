import environ
import jwt as jwtLib
from django.test import TestCase

env = environ.Env()

class LoginPostTestClass(TestCase):

    fixtures = ['authentication/fixtures/testseed.json']

    def test_validLoginRequest(self):

        response = self.client.post('/login/', { 'email': 'ajb042@student.bham.ac.uk', 'password': 'password' })
        
        expectedUserData = {
            'UserId': 2,
            'IsEmployer': False,
            'Email': "ajb042@student.bham.ac.uk"
        }

        self.assertDictEqual(response.data['userData'], expectedUserData)

        accessToken = jwtLib.decode(response.data['accessToken'], env('JWT_SECRET'), algorithms=['HS256'], verify=True)
        refreshToken = jwtLib.decode(response.data['refreshToken'], env('JWT_SECRET'), algorithms=['HS256'], verify=True)

        if not accessToken['exp'] or not accessToken['iat'] or accessToken['id'] != 2:
            raise Exception

        if not refreshToken['exp'] or not refreshToken['iat'] or refreshToken['id'] != 2:
            raise Exception


    def test_incorrectEmail(self):

        response = self.client.post('/login/', { 'email': 'gxvy123@student.bham.ac.uk', 'password': 'password' })

        self.assertEquals(response.status_code, 401)

    
    def test_incorrectPassword(self):

        response = self.client.post('/login/', { 'email': 'ajb042@student.bham.ac.uk', 'password': 'potato' })

        self.assertEquals(response.status_code, 401)
    

    def test_missingParameters(self):

        response = self.client.post('/login/')

        self.assertEquals(response.status_code, 400)
        
