import json
from copy import copy
from django.test import TestCase
from authentication.tests.jwtFuncs import createAccessToken
from authentication.models import User
from authentication.serializers import UserSerializer
from employee.models import Profile

class postProfileTests(TestCase):

    fixtures = ['authentication/fixtures/fixtures.json']

    userId = 1 # Thomas
    jwt = createAccessToken(userId)
    userData = {
        'FirstName': 'Test', 
        'LastName': 'Test',
        'Pronouns': 'They/Them',
        'PhoneNumber': '1111111111',
        'Location': 'Test',
        'TopicSentence': 'Testing TopicSentence',
        'TimeZone': 0,
        'NotableSkills': json.dumps(['Skill 1', 'Skill 2', 'Skill 3']),
        'Experience': json.dumps(['Experience 1', 'Experience 2', 'Experience 3']), 
        'Qualifications': json.dumps(['Qualification 1', 'Qualification 2', 'Qualification 3'])
        }

    def test_validRequest(self):
        profile = Profile.objects.get(UserId__exact = self.userId)
        profile.delete()

        response = self.client.post('/profile/', data=self.userData, content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 200)

    def test_missingData(self):
        profile = Profile.objects.get(UserId__exact = self.userId)
        profile.delete()

        response = self.client.post(f'/profile/', data={ }, content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEquals(response.data['status'], 400)

    def test_expiredJwt(self):
        jwt = createAccessToken(self.userId, 'now')
        response = self.client.post(
            f'/profile/',
            data=self.userData,
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'}
        )

        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'Expired auth token')

    def test_invalidJwt(self):
        jwt = self.jwt[:-1]
        response = self.client.post(
            f'/profile/',
            data=self.userData,
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'}
        )

        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'Invalid auth token')