import environ
import jwt as jwtLib
from django.test import TestCase
from employer.models import EmployerDetails
from authentication.models import RefreshToken, User

env = environ.Env()

class RegisterPostTestClass(TestCase):
    password = 'password'
    employeeEmail = 'ajb042@student.bham.ac.uk'
    employerEmail = 'sxd110@student.bham.ac.uk'

    def tearDown(self):
        User.objects.all().delete()
        EmployerDetails.objects.all().delete()
        RefreshToken.objects.all().delete()


    def test_validEmployeeRequest(self):
        response = self.client.post('/register/', { 'email': self.employeeEmail, 'password': self.password, 'isEmployer': False }, content_type='application/json')
        
        expectedUserData = {
            'IsEmployer': False,
            'Email': self.employeeEmail
        }

        self.assertEquals(response.status_code, 201)

        self.assertDictEqual(response.data['userData'], expectedUserData)

        accessToken = jwtLib.decode(response.data['accessToken'], env('JWT_SECRET'), algorithms=['HS256'], verify=True)
        refreshToken = jwtLib.decode(response.data['refreshToken'], env('JWT_SECRET'), algorithms=['HS256'], verify=True)
        
        self.assertTrue('exp' in accessToken)
        self.assertTrue('iat' in accessToken)
        self.assertTrue('id' in accessToken)
        self.assertEquals(accessToken['typ'], 'access')

        self.assertTrue('exp' in refreshToken)
        self.assertTrue('iat' in refreshToken)
        self.assertTrue('id' in refreshToken)
        self.assertEquals(refreshToken['typ'], 'refresh')

        RefreshToken.objects.get(Token__exact = response.data['refreshToken'])
    


    def test_validEmployerRequest(self):

        userData = { 
            'email': self.employerEmail, 
            'password': self.password, 
            'isEmployer': True, 
            'companyName': 'Twitter', 
            'phoneNumber': '01924 596952' 
        }

        response = self.client.post('/register/', userData, content_type='application/json')
        
        expectedUserData = {
            'IsEmployer': True,
            'Email': self.employerEmail,
            'CompanyName': 'Twitter',
            'PhoneNumber': '01924 596952'
        }

        self.assertEquals(response.status_code, 201)

        self.assertDictEqual(response.data['userData'], expectedUserData)

        accessToken = jwtLib.decode(response.data['accessToken'], env('JWT_SECRET'), algorithms=['HS256'], verify=True)
        refreshToken = jwtLib.decode(response.data['refreshToken'], env('JWT_SECRET'), algorithms=['HS256'], verify=True)
        
        self.assertTrue('exp' in accessToken)
        self.assertTrue('iat' in accessToken)
        self.assertTrue('id' in accessToken)
        self.assertEquals(accessToken['typ'], 'access')

        self.assertTrue('exp' in refreshToken)
        self.assertTrue('iat' in refreshToken)
        self.assertTrue('id' in refreshToken)
        self.assertEquals(refreshToken['typ'], 'refresh')

        EmployerDetails.objects.get(UserId__exact = accessToken['id'])
        RefreshToken.objects.get(Token__exact = response.data['refreshToken'])

    

    def test_duplicateEmailRequest(self):
        responseOne = self.client.post('/register/', { 'email': self.employeeEmail, 'password': self.password, 'isEmployer': False }, content_type='application/json')
        self.assertEquals(responseOne.status_code, 201)

        initialUsersCount = User.objects.all().count()
        responseTwo = self.client.post('/register/', { 'email': self.employeeEmail, 'password': self.password, 'isEmployer': False }, content_type='application/json')
        finalUsersCount = User.objects.all().count()

        self.assertEquals(responseTwo.status_code, 409)
        self.assertEquals(initialUsersCount, finalUsersCount)
        self.assertEquals(responseTwo.data['message'], 'account already exists for given email')

    

    def test_missingEmailRequest(self):
        initialUsersCount = User.objects.all().count()
        response = self.client.post('/register/', { 'password': self.password, 'isEmployer': False }, content_type='application/json')
        finalUsersCount = User.objects.all().count()

        self.assertEquals(response.status_code, 400)
        self.assertEquals(initialUsersCount, finalUsersCount)
        self.assertEquals(response.data['message'], 'incomplete form data: \'email\'')

    

    def test_missingPasswordRequest(self):
        initialUsersCount = User.objects.all().count()
        response = self.client.post('/register/', { 'email': 'fake@email.com', 'isEmployer': False }, content_type='application/json')
        finalUsersCount = User.objects.all().count()

        self.assertEquals(response.status_code, 400)
        self.assertEquals(initialUsersCount, finalUsersCount)
        self.assertEquals(response.data['message'], 'incomplete form data: \'password\'')



    def test_invalidCompanyNameRequest(self):
        userData = { 
            'email': 'fake@email.com', 
            'password': self.password, 
            'isEmployer': True,
            'companyName': 'super long company name that won\'t fit in the db field',
            'phoneNumber': '123456789'
        }

        initialUsersCount = User.objects.all().count()
        response = self.client.post('/register/', userData, content_type='application/json')
        finalUsersCount = User.objects.all().count()

        self.assertEquals(response.status_code, 400)
        self.assertEquals(initialUsersCount, finalUsersCount)
        self.assertEquals(response.data['message'], 'invalid form data: {\'CompanyName\': [\'Ensure this value has at most 30 characters (it has 54).\']}')