from random import randint
from django.test import TestCase
from employer.models import EmployerDetails
from employer.serializers import EmployerDetailsSerializer
from authentication.tests.jwtFuncs import createAccessToken
from authentication.models import User
from authentication.serializers import UserSerializer

class getAccountTests(TestCase):

    fixtures = ['authentication/fixtures/testseed.json']

    # user: Victoria
    userId = 6
    jwt = createAccessToken(userId)

    # GET TESTS

    def test_validRequestFullData(self):
        # make request
        response = self.client.get(f'/v1/e/accounts/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})
        data = response.data

        # check account information is correct
        detailsSet = EmployerDetails.objects.get(UserId__exact = self.userId)
        emailSet = User.objects.get(UserId__exact = self.userId)

        details = EmployerDetailsSerializer(detailsSet).data
        email  = UserSerializer(emailSet).data

        expectedData = {
            'details': details,
            'email': email['Email']
        }

        self.assertDictEqual(data, expectedData)

    def test_expiredJwt(self):
        jwt = createAccessToken(self.userId, 'now')
        response = self.client.get(f'/v1/e/accounts/', **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'Expired auth token')

    def test_invalidJwt(self):
        jwt = self.jwt[:-1]
        response = self.client.get(f'/v1/e/accounts/', **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'Invalid auth token')

class putAccountTests(TestCase):

    fixtures = ['authentication/fixtures/testseed.json']

    userId = 6 # Victoria
    jwt = createAccessToken(userId)

    # PUT TESTS

    def test_validUpdate(self):
        # Define new data vars
        newCompanyName = 'Company Name %d' % randint(1,999)
        newPhoneNumber = '%d' % randint(10000000000, 99999999999)
        newEmail = 'test%d@email.com' % randint(1,999)
        newDict = {'details': {'UserId': self.userId, 'PhoneNumber': newPhoneNumber, 'CompanyName': newCompanyName}, 'email': newEmail}

        # GET request to get old data
        getPreResponse = self.client.get(f'/v1/e/accounts/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        # PUT request to update data with vars
        putResponse = self.client.put(
            f'/v1/e/accounts/update/',
            data={
                'setCompanyName': newCompanyName,
                'setPhoneNumber': newPhoneNumber,
                'setEmail': newEmail
            },
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'}
        )

        # GET request to get new data
        getPostResponse = self.client.get(f'/v1/e/accounts/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        # Assert 200 response
        self.assertEquals(putResponse.status_code, 200)

        # Assert GET data and vars are identical
        self.assertDictEqual(getPostResponse.data, newDict)

    def test_missingRequestData(self):
        response = self.client.put(
            f'/v1/e/accounts/update/',
            data={ },
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'}
        )

        self.assertEquals(response.data['status'], 400)
        self.assertEquals(response.data['message'], 'incomplete request data')

    def test_expiredJwt(self):
        jwt = createAccessToken(self.userId, 'now')
        response = self.client.put(
            f'/v1/e/accounts/update/',
            data={
                'setCompanyName': 'Testing Inc.',
                'setPhoneNumber': 11111111111,
                'setEmail': 'testing@email.com' 
            },
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'}
        )

        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'Expired auth token')

    def test_invalidJwt(self):
        jwt = self.jwt[:-1]
        response = self.client.put(
            f'/v1/e/accounts/update/',
            data={
                'setCompanyName': 'Testing Inc.',
                'setPhoneNumber': 11111111111,
                'setEmail': 'testing@email.com'
            },
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'}
        )

        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'Invalid auth token')

class deleteAccountTests(TestCase):

    fixtures = ['authentication/fixtures/testseed.json']

    userId = 5 # Yue
    jwt = createAccessToken(userId)

    # DELETE TESTS

    def test_validDelete(self):
        # DELETE request to delete data
        deleteResponse = self.client.delete(f'/v1/e/accounts/delete/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        # Assert response code 200
        self.assertEquals(deleteResponse.status_code, 200)


    def test_expiredJwt(self):
        jwt = createAccessToken(self.userId, 'now')
        response = self.client.delete(f'/v1/e/accounts/delete/', **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'Expired auth token')

    def test_invalidJwt(self):
        jwt = self.jwt[:-1]
        response = self.client.delete(f'/v1/e/accounts/delete/', **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'Invalid auth token')