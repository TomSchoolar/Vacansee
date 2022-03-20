import jwt
import environ
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

        returnedJwt = jwt.decode(response.data['jwt'], env('JWT_SECRET'), algorithms=['HS256'], verify=True)

        if not returnedJwt['exp'] or not returnedJwt['iat'] or returnedJwt['id'] != 2:
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
        
