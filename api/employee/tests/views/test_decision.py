from django.test import TestCase
from authentication.tests.jwtFuncs import createAccessToken
from employee.models import Favourite, Application, Reject



class decisionTestCase(TestCase):

    userId = 1
    vacancyId = 1006
    jwt = createAccessToken(userId)
    fixtures = ['authentication/fixtures/testseed.json']

    def test_favouriting(self):
        response = self.client.post(f'/v1/vacancies/{ 1000 }/favourite/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 201)

        Favourite.objects.filter(UserId__exact = self.userId, VacancyId__exact = self.vacancyId).delete()



    def test_apply(self):
        response = self.client.post(f'/v1/vacancies/{ self.vacancyId }/apply/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 201)

        Application.objects.filter(UserId__exact = self.userId, VacancyId__exact = self.vacancyId).delete()



    def test_applyToFavouritedVacancy(self):
        response1 = self.client.post(f'/v1/vacancies/{ self.vacancyId }/favourite/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})
        self.assertEqual(response1.status_code, 201)      

        response2 = self.client.post(f'/v1/vacancies/{ self.vacancyId }/apply/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})
        self.assertEqual(response2.status_code, 201)

        favCount = Favourite.objects.filter(UserId__exact = self.userId, VacancyId__exact = self.vacancyId).count()
        self.assertEquals(favCount, 0)

        Application.objects.filter(UserId__exact = self.userId, VacancyId__exact = self.vacancyId).delete()



    def test_repeatedApply(self):
        response1 = self.client.post(f'/v1/vacancies/{ self.vacancyId }/apply/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response1.status_code, 201)

        response2 = self.client.post(f'/v1/vacancies/{ self.vacancyId }/apply/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEquals(response2.status_code, 400)
        self.assertEquals(response2.data['message'], 'Application to that vacancy already exists')
        
        Application.objects.filter(UserId__exact = self.userId, VacancyId__exact = self.vacancyId).delete()

    

    def test_applyToRejectedVacancy(self):
        response1 = self.client.post(f'/v1/vacancies/{ self.vacancyId }/reject/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response1.status_code, 201)

        response2 = self.client.post(f'/v1/vacancies/{ self.vacancyId }/apply/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEquals(response2.status_code, 400)
        self.assertEquals(response2.data['message'], 'Cannot apply to a vacancy that you\'ve already rejected')
        
        Reject.objects.filter(UserId__exact = self.userId, VacancyId__exact = self.vacancyId).delete()



    def test_validReject(self):
        response = self.client.post(f'/v1/vacancies/{ self.vacancyId }/reject/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 201)
        
        Reject.objects.filter(UserId__exact = self.userId, VacancyId__exact = self.vacancyId).delete()



    def test_rejectFavouritedVacancy(self):
        response1 = self.client.post(f'/v1/vacancies/{ self.vacancyId }/favourite/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})
        self.assertEqual(response1.status_code, 201)      

        response2 = self.client.post(f'/v1/vacancies/{ self.vacancyId }/reject/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})
        self.assertEqual(response2.status_code, 201)

        favCount = Favourite.objects.filter(UserId__exact = self.userId, VacancyId__exact = self.vacancyId).count()
        self.assertEquals(favCount, 0)

        Application.objects.filter(UserId__exact = self.userId, VacancyId__exact = self.vacancyId).delete()



    def test_repeatedReject(self):
        response1 = self.client.post(f'/v1/vacancies/{ self.vacancyId }/reject/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})
        
        self.assertEqual(response1.status_code, 201)

        response2 = self.client.post(f'/v1/vacancies/{ self.vacancyId }/reject/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEquals(response2.status_code, 400)
        self.assertEquals(response2.data['message'], 'User has already rejected that vacancy')
        
        Reject.objects.filter(UserId__exact = self.userId, VacancyId__exact = self.vacancyId).delete()



    def test_rejectAppliedToVacancy(self):
        response1 = self.client.post(f'/v1/vacancies/{ self.vacancyId }/apply/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response1.status_code, 201)

        response2 = self.client.post(f'/v1/vacancies/{ self.vacancyId }/reject/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEquals(response2.status_code, 400)
        self.assertEquals(response2.data['message'], 'Cannot reject a vacancy that you have already applied to')
        
        Application.objects.filter(UserId__exact = self.userId, VacancyId__exact = self.vacancyId).delete()



    def test_invalidReject(self):
        response = self.client.post(f'/v1/vacancies/{ 9999 }/reject/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], 'That vacancy is not open for applications')



    def test_expiredJWT(self):
        jwt = createAccessToken(self.userId, 'now')

        response = self.client.post(f'/v1/vacancies/{ self.vacancyId }/reject/', **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Expired auth token')



    def test_invalidJWT(self):
        jwt = self.jwt[:-1]

        response = self.client.post(f'/v1/vacancies/{ self.vacancyId }/reject/', **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }'})

        self.assertEqual(response.data['status'], 401)
        self.assertEqual(response.data['message'], 'Invalid auth token')