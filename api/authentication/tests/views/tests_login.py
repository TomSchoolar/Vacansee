import environ
import jwt as jwtLib
from django.test import TestCase
from employer.models import EmployerDetails
from authentication.models import RefreshToken
from employee.models import Profile

env = environ.Env()

class LoginPostTestClass(TestCase):

    password = 'password'
    employeeId = 2
    employeeEmail = 'ajb042@student.bham.ac.uk'
    employerId = 4
    employerEmail = 'sxd110@student.bham.ac.uk'
    noProfileId = 3
    noProfileEmail = 'cxd066@student.bham.ac.uk';

    fixtures = ['authentication/fixtures/fixtures.json']


    def tearDown(self):
        RefreshToken.objects.all().delete()


    def test_validLoginRequest(self):

        response = self.client.post('/v1/login/', { 'email': self.employeeEmail, 'password': self.password })
        
        expectedUserData = {
            'IsEmployer': False,
            'Email': self.employeeEmail,
            'HasProfileSetup': True
        }

        self.assertDictEqual(response.data['userData'], expectedUserData)

        accessToken = jwtLib.decode(response.data['accessToken'], env('JWT_SECRET'), algorithms=['HS256'], verify=True)
        refreshToken = jwtLib.decode(response.data['refreshToken'], env('JWT_SECRET'), algorithms=['HS256'], verify=True)

        
        self.assertTrue('exp' in accessToken)
        self.assertTrue('iat' in accessToken)
        self.assertEquals(accessToken['id'], self.employeeId)
        self.assertEquals(accessToken['typ'], 'access')

        self.assertTrue('exp' in refreshToken)
        self.assertTrue('iat' in refreshToken)
        self.assertEquals(refreshToken['id'], self.employeeId)
        self.assertEquals(refreshToken['typ'], 'refresh')

        RefreshToken.objects.get(Token__exact = response.data['refreshToken'])


    
    def test_validEmployerLoginRequest(self):

        response = self.client.post('/v1/login/', { 'email': self.employerEmail, 'password': self.password })
        
        details = EmployerDetails.objects.get(UserId__exact = self.employerId)

        expectedUserData = {
            'IsEmployer': True,
            'Email': self.employerEmail,
            'CompanyName': details.CompanyName,
            'PhoneNumber': details.PhoneNumber,
            'HasProfileSetup': True
        }

        self.assertDictEqual(response.data['userData'], expectedUserData)

        accessToken = jwtLib.decode(response.data['accessToken'], env('JWT_SECRET'), algorithms=['HS256'], verify=True)
        refreshToken = jwtLib.decode(response.data['refreshToken'], env('JWT_SECRET'), algorithms=['HS256'], verify=True)

        
        self.assertTrue('exp' in accessToken)
        self.assertTrue('iat' in accessToken)
        self.assertEquals(accessToken['id'], self.employerId)
        self.assertEquals(accessToken['typ'], 'access')

        self.assertTrue('exp' in refreshToken)
        self.assertTrue('iat' in refreshToken)
        self.assertEquals(refreshToken['id'], self.employerId)
        self.assertEquals(refreshToken['typ'], 'refresh')

        RefreshToken.objects.get(Token__exact = response.data['refreshToken'])




    def test_incorrectEmail(self):
        response = self.client.post('/v1/login/', { 'email': 'gxvy123@student.bham.ac.uk', 'password': self.password })

        self.assertEquals(response.status_code, 401)


    
    def test_incorrectPassword(self):
        response = self.client.post('/v1/login/', { 'email': self.employeeEmail, 'password': 'potato' })

        self.assertEquals(response.status_code, 401)
    


    def test_missingParameters(self):
        response = self.client.post('/v1/login/')

        self.assertEquals(response.status_code, 400)
    


    def test_loginTwoAccountsCheckRefreshFamily(self):
        # login to two accounts consecutively and make sure the refresh token records have different, and correct family ids
        
        firstResponse = self.client.post('/v1/login/', { 'email': self.employeeEmail, 'password': self.password })
        
        firstRefreshToken = firstResponse.data['refreshToken']
        firstTokenFamily = RefreshToken.objects.get(Token__exact = firstRefreshToken).FamilyId

        self.assertEquals(firstTokenFamily, 0)

        secondResponse = self.client.post('/v1/login/', { 'email': self.employerEmail, 'password': self.password })
        
        secondRefreshToken = secondResponse.data['refreshToken']
        secondTokenFamily = RefreshToken.objects.get(Token__exact = secondRefreshToken).FamilyId

        self.assertEquals(secondTokenFamily, 1)



    def test_validNoProfileLoginRequest(self):
        # delete profile first.
        profile = Profile.objects.get(UserId__exact = self.noProfileId)
        profile.delete()

        response = self.client.post('/v1/login/', { 'email': self.noProfileEmail, 'password': self.password })
        
        expectedUserData = {
            'IsEmployer': False,
            'Email': self.noProfileEmail,
            'HasProfileSetup': False
        }

        self.assertDictEqual(response.data['userData'], expectedUserData)

        accessToken = jwtLib.decode(response.data['accessToken'], env('JWT_SECRET'), algorithms=['HS256'], verify=True)
        refreshToken = jwtLib.decode(response.data['refreshToken'], env('JWT_SECRET'), algorithms=['HS256'], verify=True)

        
        self.assertTrue('exp' in accessToken)
        self.assertTrue('iat' in accessToken)
        self.assertEquals(accessToken['id'], self.noProfileId)
        self.assertEquals(accessToken['typ'], 'access')

        self.assertTrue('exp' in refreshToken)
        self.assertTrue('iat' in refreshToken)
        self.assertEquals(refreshToken['id'], self.noProfileId)
        self.assertEquals(refreshToken['typ'], 'refresh')

        RefreshToken.objects.get(Token__exact = response.data['refreshToken'])