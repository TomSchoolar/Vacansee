from json import dumps
from copy import copy
from django.test import TestCase
from authentication.tests.jwtFuncs import createAccessToken
from authentication.models import User
from authentication.serializers import UserSerializer
from employee.models import Profile
from employee.serializers import ProfileSerializer

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
        'NotableSkills': dumps(['Skill 1', 'Skill 2', 'Skill 3']),
        'Experience': dumps(['Experience 1', 'Experience 2', 'Experience 3']), 
        'Qualifications': dumps(['Qualification 1', 'Qualification 2', 'Qualification 3'])
        }

    def test_validRequest(self):
        profile = Profile.objects.get(UserId__exact = self.userId)
        profile.delete()

        response = self.client.post('/v1/profiles/', data=self.userData, content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 200)

    def test_missingData(self):
        profile = Profile.objects.get(UserId__exact = self.userId)
        profile.delete()

        response = self.client.post(f'/v1/profiles/', data={ }, content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEquals(response.data['status'], 400)

    def test_expiredJwt(self):
        jwt = createAccessToken(self.userId, 'now')
        response = self.client.post(
            f'/v1/profiles/',
            data=self.userData,
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'}
        )

        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'Expired auth token')

    def test_invalidJwt(self):
        jwt = self.jwt[:-1]
        response = self.client.post(
            f'/v1/profiles/',
            data=self.userData,
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'}
        )

        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'Invalid auth token')

class postProfileEditTests(TestCase):
    fixtures = ['authentication/fixtures/fixtures.json']

    userId = 1 # Thomas
    jwt = createAccessToken(userId)
    userData = {
        'FirstName': 'Test2', 
        'LastName': 'Test2',
        'Pronouns': 'Xe/Xem',
        'PhoneNumber': '1111111112',
        'Location': 'Test2',
        'TopicSentence': 'Testing TopicSentence Again',
        'TimeZone': 0,
        'NotableSkills': dumps(['Skill 11', 'Skill 22', 'Skill 33']),
        'Experience': dumps(['Experience 11', 'Experience 22', 'Experience 33']), 
        'Qualifications': dumps(['Qualification 1', 'Qualification 2', 'Qualification 3'])
        }

    def test_validRequest(self):
        oldProfileSet = Profile.objects.get(UserId__exact = self.userId)
        oldProfile = ProfileSerializer(oldProfileSet).data

        modifiedProfile = copy(oldProfile)

        del modifiedProfile['UserId']

        modifiedProfile['NotableSkills'] = dumps(modifiedProfile['NotableSkills'])
        modifiedProfile['Experience'] = dumps(modifiedProfile['Experience'])
        modifiedProfile['Qualifications'] = dumps(modifiedProfile['Qualifications'])

        response = self.client.post(f'/v1/profiles/edit/', data=modifiedProfile, content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 200)

        newProfileSet = Profile.objects.get(UserId__exact = self.userId)
        newProfile = ProfileSerializer(newProfileSet).data

        self.assertDictEqual(oldProfile, newProfile)

    def test_invalidData(self):
        oldProfileSet = Profile.objects.get(UserId__exact = self.userId)
        oldProfile = ProfileSerializer(oldProfileSet).data

        modifiedProfile = copy(oldProfile)

        del modifiedProfile['UserId']

        modifiedProfile['NotableSkills'].append('Skill 4')

        modifiedProfile['NotableSkills'] = dumps(modifiedProfile['NotableSkills'])
        modifiedProfile['Experience'] = dumps(modifiedProfile['Experience'])
        modifiedProfile['Qualifications'] = dumps(modifiedProfile['Qualifications'])

        response = self.client.post(f'/v1/profiles/edit/', data=modifiedProfile, content_type='application/json', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEquals(response.data['status'], 400)
        self.assertEquals(response.data['message'], 'Invalid profile data')

        newProfileSet = Profile.objects.get(UserId__exact = self.userId)
        newProfile = ProfileSerializer(newProfileSet).data

        oldProfile['NotableSkills'].pop()

        self.assertDictEqual(oldProfile, newProfile)

    def test_expiredJwt(self):
        jwt = createAccessToken(self.userId, 'now')
        response = self.client.post(
            f'/v1/profiles/edit/',
            data=self.userData,
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'}
        )

        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'Expired auth token')

    def test_invalidJwt(self):
        jwt = self.jwt[:-1]
        response = self.client.post(
            f'/v1/profiles/edit/',
            data=self.userData,
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'}
        )

        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'Invalid auth token')