from venv import create
from django.test import TestCase
from django.db.models import Count, Q
from employee.serializers import ApplicationSerializer, ProfileSerializer
from authentication.models import User
from employee.models import Profile, Application
from employer.serializers import VacancySerializer
from employer.models import Vacancy
from authentication.tests.jwtFuncs import createAccessToken

class getVacanciesTests(TestCase):
    userId = 6 # User: Victoria
    vacancyId = 1007 # Paramedic
    jwt = createAccessToken(userId)
    fixtures = ['authentication/fixtures/testseed.json']



    def test_validRequestSortMatchesDesc(self):
        response = self.client.get('/v1/e/matches/', { 'sort': 'matchesDesc', 'searchValue': '' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }' })

        vacancies = Vacancy.objects.filter(UserId__exact = 6).annotate(MatchesCount = Count('application', filter = Q(
            application__ApplicationStatus__exact = 'MATCHED',
            application__VacancyId__UserId__exact = 6
        ))).order_by('-MatchesCount').values()
        numVacancies = vacancies.count()

        expectedData = { 'vacancies': vacancies, 'numVacancies': numVacancies }

        self.assertQuerysetEqual(expectedData['vacancies'], response.data['vacancies'])
        self.assertEqual(expectedData['numVacancies'], response.data['numVacancies'])



    def test_validRequestSortDateDesc(self):
        response = self.client.get('/v1/e/matches/', { 'sort': 'dateDesc', 'searchValue': '' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }' })
        
        vacancies = Vacancy.objects.filter(UserId__exact = 6).annotate(
        MatchesCount = Count('application', filter = Q(
            application__ApplicationStatus__exact = 'MATCHED',
            application__VacancyId__UserId__exact = 6
        ))).order_by('-Created').values()
        numVacancies = vacancies.count()

        expectedData = { 'vacancies': vacancies, 'numVacancies': numVacancies }

        self.assertQuerysetEqual(expectedData['vacancies'], response.data['vacancies'])
        self.assertEqual(expectedData['numVacancies'], response.data['numVacancies'])



    def test_validRequestSortDateAsc(self):
        response = self.client.get('/v1/e/matches/', { 'sort': 'dateAsc', 'searchValue': '' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }' })

        vacancies = Vacancy.objects.filter(UserId__exact = 6).annotate(
        MatchesCount = Count('application', filter = Q(
            application__ApplicationStatus__exact = 'MATCHED',
            application__VacancyId__UserId__exact = 6
        ))).order_by('Created').values()
        numVacancies = vacancies.count()

        expectedData = { 'vacancies': vacancies, 'numVacancies': numVacancies }

        self.assertQuerysetEqual(expectedData['vacancies'], response.data['vacancies'])
        self.assertEqual(expectedData['numVacancies'], response.data['numVacancies'])



    def test_validRequestSortTitleAsc(self):
        response = self.client.get('/v1/e/matches/', { 'sort': 'titleAsc', 'searchValue': '' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }' })

        vacancies = Vacancy.objects.filter(UserId__exact = 6).annotate(
        MatchesCount = Count('application', filter = Q(
            application__ApplicationStatus__exact = 'MATCHED',
            application__VacancyId__UserId__exact = 6
        ))).order_by('VacancyName').values()
        numVacancies = vacancies.count()

        expectedData = { 'vacancies': vacancies, 'numVacancies': numVacancies }

        self.assertQuerysetEqual(expectedData['vacancies'], response.data['vacancies'])
        self.assertEqual(expectedData['numVacancies'], response.data['numVacancies'])



    def test_validRequestSortTitleDesc(self):
        response = self.client.get('/v1/e/matches/', { 'sort': 'titleDesc', 'searchValue': '' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }' })

        vacancies = Vacancy.objects.filter(UserId__exact = 6).annotate(
        MatchesCount = Count('application', filter = Q(
            application__ApplicationStatus__exact = 'MATCHED',
            application__VacancyId__UserId__exact = 6
        ))).order_by('-VacancyName').values()
        numVacancies = vacancies.count()

        expectedData = { 'vacancies': vacancies, 'numVacancies': numVacancies }

        self.assertQuerysetEqual(expectedData['vacancies'], response.data['vacancies'])
        self.assertEqual(expectedData['numVacancies'], response.data['numVacancies'])



    def test_validRequestSearchValue(self):
        response = self.client.get('/v1/e/matches', { 'sort': 'titleDesc', 'searchValue': 'e' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }' })

        vacancies = Vacancy.objects.filter(UserId__exact = 6).annotate(
        MatchesCount = Count('application', filter = Q(
            application__ApplicationStatus__exact = 'MATCHED',
            application__VacancyId__UserId__exact = 6,
            application__VacancyId__VacancyName__contains = 'e'
        ))).order_by('-VacancyName').values()
        numVacancies = vacancies.count()

        expectedData = { 'vacancies': vacancies, 'numVacancies': numVacancies }

        self.assertQuerysetEqual(expectedData['vacancies'], response.data['vacancies'])
        self.assertEqual(expectedData['numVacancies'], response.data['numVacancies'])



    def test_missingParamters(self):
        response = self.client.get('/v1/e/matches/', { }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEquals(response.status_code, 400)
    


    def test_expiredJWT(self):
        jwt = createAccessToken(self.userId, 'now')
        response = self.client.get('/v1/e/matches/', { 'sort': 'dateDesc', 'searchValue': '' }, **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }' })

        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'Expired auth token')



    def test_invalidJWT(self):
        jwt = self.jwt[:-1]
        response = self.client.get('/v1/e/matches/', { 'sort': 'dateDesc', 'searchValue': '' }, **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }' })

        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'Invalid auth token')



class getMatchesTests(TestCase):
    userId = 6 # User: Victoria
    vacId = 1007 # Vacancy: Paramedic
    jwt = createAccessToken(userId)
    fixtures = ['authentication/fixtures/testseed.json']

    def test_validRequest(self):
        response = self.client.get(f'/v1/e/matches/{ self.vacId }/', { 'sort': 'dateDesc', 'searchValue': '' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }' })

        matchesSet = Application.objects.filter(
            VacancyId__exact = self.vacId,
            ApplicationStatus__exact = 'MATCHED'
        )

        matches = ApplicationSerializer(matchesSet, many=True).data
        numMatches = matchesSet.count()

        expectedData = { 'matches': matches, 'numMatches': numMatches }

        self.assertDictEqual(expectedData, response.data)



    def test_validRequestSearchValue(self):
        response = self.client.get(f'/v1/e/matches/{ self.vacId }/', { 'sort': 'dateDesc', 'searchValue': 'e' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }' })

        userIdList = []

        userSet = Profile.objects.filter(LastName__contains = 'e')

        for user in userSet:
            userIdList.append(user.UserId)

        matchesSet = Application.objects.filter(
            VacancyId__exact = self.vacId,
            ApplicationStatus__exact = 'MATCHED',
            UserId__in = userIdList
        )

        matches = ApplicationSerializer(matchesSet, many=True).data
        numMatches = matchesSet.count()

        expectedData = { 'matches': matches, 'numMatches': numMatches }

        self.assertDictEqual(expectedData, response.data)



    def test_missingParameters(self):
        response = self.client.get('/v1/e/matches/', { }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }' })
 
        self.assertEquals(response.status_code, 400)



    def test_expiredJWT(self):
        jwt = createAccessToken(self.userId, 'now')
        response = self.client.get(f'/v1/e/matches/{ self.vacId }/', { 'sort': 'dateDesc' }, **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }' })

        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'Expired auth token')



    def test_invalidJWT(self):
        jwt = self.jwt[:-1]
        response = self.client.get(f'/v1/e/matches/{ self.vacId }/', { 'sort': 'dateDesc' }, **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }' })

        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'Invalid auth token')



class getCardTests(TestCase):
    userId = 6 # User: Victoria
    applicantId = 3
    jwt = createAccessToken(userId)
    fixtures = ['authentication/fixtures/testseed.json']



    def test_validRequest(self):
        response = self.client.get(f'/v1/e/matches/card/{ self.applicantId }/', **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }' })

        detailsSet = Profile.objects.get(UserId__exact = self.applicantId)
        details = ProfileSerializer(detailsSet, many=False).data

        expectedData = { 'details': details }

        self.assertDictEqual(expectedData, response.data)



    def test_expiredJWT(self):
        jwt = createAccessToken(self.userId, 'now')
        response = self.client.get(f'/v1/e/matches/card/{ self.applicantId }/', **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }' })

        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'Expired auth token')



    def test_invalidJWT(self):
        jwt = self.jwt[:-1]
        response = self.client.get(f'/v1/e/matches/card/{ self.applicantId }/', **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }' })

        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'Invalid auth token')

