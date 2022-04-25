from django.test import TestCase
from authentication.models import User
from datetime import datetime, timezone, timedelta
from secrets import token_urlsafe
from hashlib import sha256

def createNewToken(email):
    plainToken = token_urlsafe(75)
    hashedToken = sha256(plainToken.encode()).hexdigest()
    user = User.objects.get(Email__exact=email)
    expiry = datetime.now(tz=timezone.utc) + timedelta(minutes=10)
    user.PasswordResetToken = hashedToken
    user.PasswordResetExpiration = expiry.strftime('%Y-%m-%dT%H:%M:%S+0000')
    user.save(update_fields=['PasswordResetToken','PasswordResetExpiration'])

    return plainToken


class postEmailTests(TestCase):
    
    email = 'vrt911@student.bham.ac.uk'
    fixtures = ['authentication/fixtures/testseed.json']

    # TESTS:
    # Valid Request (Send email to vrt911@student.bham.ac.uk)
    def test_validRequest(self):
        preUser = User.objects.get(Email__exact=self.email)
        noResetToken = preUser.PasswordResetToken
        noExpiration = preUser.PasswordResetExpiration
        
        response = self.client.post(f'/forgot/', data={'email': self.email})

        postUser = User.objects.get(Email__exact=self.email)
        resetToken = postUser.PasswordResetToken
        expiration = postUser.PasswordResetExpiration

        self.assertNotEqual(noExpiration, expiration)
        self.assertNotEqual(noResetToken, resetToken)
        self.assertEqual(response.status_code, 200)


    # Missing Data
    def test_missingData(self):
        response = self.client.post(f'/forgot/')

        self.assertEqual(response.data['status'], 400)
        self.assertEqual(response.data['message'], 'incomplete form data')

    # Invalid Email
    def test_invalidEmail(self):
        invalidEmail = 'test@test.com'
        response = self.client.post(f'/forgot/', data={'email': invalidEmail})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Unauthorised request.')

class getResetTests(TestCase):

    email = 'vrt911@student.bham.ac.uk'
    fixtures = ['authentication/fixtures/testseed.json']

    # TESTS:
    # Valid Request
    def test_validRequest(self):
        token = createNewToken(self.email)
        response = self.client.get(f'/reset/{token}/')

        self.assertEqual(response.status_code, 200)

    # Expiration Passed (Update DB with old token, test against new token)
    def test_tokenExpired(self):
        token = createNewToken(self.email)
        user = User.objects.get(Email__exact=self.email)
        oldTime = datetime.now(tz=timezone.utc) - timedelta(minutes=2)
        user.PasswordResetExpiration = oldTime
        user.save(update_fields=['PasswordResetExpiration'])

        response = self.client.get(f'/reset/{token}/')

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Expired reset token.')

    # Invalid Token
    def test_invalidToken(self):
        invalidToken = 'a'
        response = self.client.get(f'/reset/{invalidToken}/')

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Unauthorised request.')

class postResetTests(TestCase):

    email = 'vrt911@student.bham.ac.uk'
    fixtures = ['authentication/fixtures/testseed.json']

    # TESTS:
    # Valid Request
    def test_validRequest(self):
        newPassword = 'testingPassword'
        token = createNewToken(self.email)

        response = self.client.post(f'/reset/', data={'password': newPassword, 'token': token})

        self.assertEqual(response.data['status'], 200)
        self.assertEqual(response.data['message'], 'Update successful.')

    # Missing Data
    def test_missingData(self):
        response = self.client.post(f'/reset/')

        self.assertEqual(response.data['status'], 400)
        self.assertEqual(response.data['message'], 'incomplete request data')

    # Expiration Passed (Update DB with old time, test against token)
    def test_tokenExpired(self):
        token = createNewToken(self.email)
        user = User.objects.get(Email__exact=self.email)
        oldTime = datetime.now(tz=timezone.utc) - timedelta(minutes=2)
        user.PasswordResetExpiration = oldTime
        user.save(update_fields=['PasswordResetExpiration'])

        response = self.client.post(f'/reset/', data={'password': 'testing', 'token': token})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Expired reset token.')

    # Invalid Token
    def test_invalidToken(self):
        invalidToken = 'a'
        response = self.client.post(f'/reset/', data={'password': 'testing', 'token': invalidToken})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Unauthorised request.')
