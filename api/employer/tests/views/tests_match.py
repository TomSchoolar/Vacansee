from venv import create
from django.test import TestCase
from django.db.models import Count, Q
from employee.serializers import ApplicationSerializer, ProfileSerializer
from employee.models import Profile, Application
from employer.serializers import VacancySerializer
from employer.models import Vacancy
from authentication.tests.jwtFuncs import createAccessToken

class getVacanciesTests(TestCase):
    userId = 6 # User: Victoria
    vacancyId = 1007 # Paramedic
    jwt = createAccessToken(userId)
    fixtures = ['authentication/fixtures/testseed.json']
    maxDiff = None
    
    # Tests Needed:
    # Valid Request DONE
    # Sort by Match Count Desc
    # Sort by Date Desc DONE
    # Sort by Date Asc DONE
    # Sort by Title Asc DONE
    # Sort by Title Desc DONE
    # Missing GET Parameters DONE
    # Invalid JWT DONE
    # Expired JWT DONE
    # Check data is expected DONE

    # BROKEN
    def test_validRequestSortMatchesDesc(self):
        response = self.client.get('/e/match/', { 'sort': 'matchesDesc' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }' })

        vacancies = Vacancy.objects.filter(UserId__exact = 6).annotate(MatchesCount = Count('application', filter = Q(
            application__ApplicationStatus__exact = 'MATCHED',
            application__VacancyId__UserId__exact = 6
        ))).order_by('-MatchesCount').values()
        numVacancies = vacancies.count()
        #vacancies = VacancySerializer(vacancySet, many=True).data

        expectedData = { 'vacancies': vacancies, 'numVacancies': numVacancies }

        self.assertQuerysetEqual(expectedData['vacancies'], response.data['vacancies'])
        self.assertEqual(expectedData['numVacancies'], response.data['numVacancies'])

    # BROKEN
    def test_validRequestSortDateDesc(self):
        response = self.client.get('/e/match/', { 'sort': 'dateDesc' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }' })
        
        vacancies = Vacancy.objects.filter(UserId__exact = 6).annotate(
        MatchesCount = Count('application', filter = Q(
            application__ApplicationStatus__exact = 'MATCHED',
            application__VacancyId__UserId__exact = 6
        ))).order_by('-Created').values()
        numVacancies = vacancies.count()
        #vacancies = VacancySerializer(vacancySet, many=True).data

        expectedData = { 'vacancies': vacancies, 'numVacancies': numVacancies }

        self.assertQuerysetEqual(expectedData['vacancies'], response.data['vacancies'])
        self.assertEqual(expectedData['numVacancies'], response.data['numVacancies'])

    # BROKEN
    def test_validRequestSortDateAsc(self):
        response = self.client.get('/e/match/', { 'sort': 'dateAsc' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }' })

        vacancies = Vacancy.objects.filter(UserId__exact = 6).annotate(
        MatchesCount = Count('application', filter = Q(
            application__ApplicationStatus__exact = 'MATCHED',
            application__VacancyId__UserId__exact = 6
        ))).order_by('Created').values()
        numVacancies = vacancies.count()
        #vacancies = VacancySerializer(vacancySet, many=True).data

        expectedData = { 'vacancies': vacancies, 'numVacancies': numVacancies }

        self.assertQuerysetEqual(expectedData['vacancies'], response.data['vacancies'])
        self.assertEqual(expectedData['numVacancies'], response.data['numVacancies'])

    # BROKEN
    def test_validRequestSortTitleAsc(self):
        response = self.client.get('/e/match/', { 'sort': 'titleAsc' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }' })

        vacancies = Vacancy.objects.filter(UserId__exact = 6).annotate(
        MatchesCount = Count('application', filter = Q(
            application__ApplicationStatus__exact = 'MATCHED',
            application__VacancyId__UserId__exact = 6
        ))).order_by('VacancyName').values()
        numVacancies = vacancies.count()
        #vacancies = VacancySerializer(vacancySet, many=True).data

        expectedData = { 'vacancies': vacancies, 'numVacancies': numVacancies }

        self.assertQuerysetEqual(expectedData['vacancies'], response.data['vacancies'])
        self.assertEqual(expectedData['numVacancies'], response.data['numVacancies'])

    # BROKEN
    def test_validRequestSortTitleDesc(self):
        response = self.client.get('/e/match/', { 'sort': 'titleDesc' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }' })

        vacancies = Vacancy.objects.filter(UserId__exact = 6).annotate(
        MatchesCount = Count('application', filter = Q(
            application__ApplicationStatus__exact = 'MATCHED',
            application__VacancyId__UserId__exact = 6
        ))).order_by('-VacancyName').values()
        numVacancies = vacancies.count()
        #vacancies = VacancySerializer(vacancySet, many=True).data

        expectedData = { 'vacancies': vacancies, 'numVacancies': numVacancies }

        self.assertQuerysetEqual(expectedData['vacancies'], response.data['vacancies'])
        self.assertEqual(expectedData['numVacancies'], response.data['numVacancies'])

    def test_missingParamters(self):
        response = self.client.get('/e/match/', { }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        self.assertEquals(response.status_code, 400)
    
    def test_expiredJWT(self):
        jwt = createAccessToken(self.userId, 'now')
        response = self.client.get('/e/match/', { 'sort': 'dateDesc' }, **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }' })

        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'Expired auth token')

    def test_invalidJWT(self):
        jwt = self.jwt[:-1]
        response = self.client.get('/e/match/', { 'sort': 'dateDesc' }, **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }' })

        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'Invalid auth token')

class getMatchesTests(TestCase):
    userId = 6 # User: Victoria
    vacId = 1007 # Vacancy: Paramedic
    jwt = createAccessToken(userId)
    fixtures = ['authentication/fixtures/testseed.json']

    # Tests Needed:
    # Valid Request DONE
    # Missing GET Parameters DONE
    # Expected data DONE
    # Sorting
    # Invalid & Expired JWTs DONE

    def test_validRequest(self):
        response = self.client.get('/e/match/matches/', { 'sort': 'dateDesc', 'vID': self.vacId }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }' })

        matchesSet = Application.objects.filter(
            VacancyId__exact = self.vacId,
            ApplicationStatus__exact = 'MATCHED'
        )

        matches = ApplicationSerializer(matchesSet, many=True).data
        numMatches = matchesSet.count()

        expectedData = { 'matches': matches, 'numMatches': numMatches }

        self.assertDictEqual(expectedData, response.data)

    def test_missingParameters(self):
        response = self.client.get('/e/match/matches/', { }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }' })
 
        self.assertEquals(response.status_code, 400)

    def test_expiredJWT(self):
        jwt = createAccessToken(self.jwt, 'now')
        response = self.client.get('/e/match/matches/', { 'sort': 'dateDesc', 'vID': self.vacId }, **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }' })

        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'Expired auth token')

    def test_invalidJWT(self):
        jwt = self.jwt[:-1]
        response = self.client.get('/e/match/matches/', { 'sort': 'dateDesc', 'vID': self.vacId }, **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }' })

        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'Invalid auth token')

class getCardTests(TestCase):
    userId = 6 # User: Victoria
    applicantId = 3
    jwt = createAccessToken(userId)
    fixtures = ['authentication/fixtures/testseed.json']

    # Tests Needed:
    # Valid Request DONE
    # Missing GET Parameters DONE
    # Invalid & Expired JWTs DONE

    def test_validRequest(self):
        response = self.client.get('/e/match/card/', { 'applicantId': self.applicantId }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }' })

        detailsSet = Profile.objects.filter(UserId__exact = self.applicantId)
        details = ProfileSerializer(detailsSet, many=True).data

        expectedData = { 'details': details }

        self.assertDictEqual(expectedData, response.data)

    def test_missingParameters(self):
        response = self.client.get('/e/match/card/', { }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }' })

        self.assertEquals(response.status_code, 400)

    def test_expiredJWT(self):
        jwt = createAccessToken(self.jwt, 'now')
        response = self.client.get('/e/match/card/', { 'applicantId': self.applicantId }, **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }' })

        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'Expired auth token')

    def test_invalidJWT(self):
        jwt = self.jwt[:-1]
        response = self.client.get('/e/match/matches/', { 'applicantId': self.applicantId }, **{'HTTP_AUTHORIZATION': f'Bearer: { jwt }' })

        self.assertEquals(response.data['status'], 401)
        self.assertEquals(response.data['message'], 'Invalid auth token')

