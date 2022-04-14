from django.test import TestCase
from employer.models import Vacancy
from authentication.tests.jwtFuncs import createAccessToken
from employee.models import Favourite, Reject, Application



class applicationTestCase(TestCase):

    fixtures = ['authentication/fixtures/testseed.json']
    jwt = createAccessToken(1019)

    def test_getApplications(self):
        response = self.client.get('/vacancy/', { 'uID':1019, 'sort':'titleAsc', 'count':5, 'pageNum':1, 'filter':'all' }, **{'HTTP_AUTHORIZATION': f'Bearer: { self.jwt }'})

        vacancyList = []

        favouriteSet = Favourite.objects.filter(
            UserId__exact = 1019
        )

        rejectSet = Reject.objects.filter(
            UserId__exact = 1019
        )

        applicationSet = Application.objects.filter(
            UserId__exact = 1019
        )

        for fav in favouriteSet:
            vacancyList.append(fav.VacancyId.VacancyId)

        for rej in rejectSet:
            vacancyList.append(rej.VacancyId.VacancyId)

        for app in applicationSet:
            vacancyList.append(app.VacancyId.VacancyId)

        vacancySet = Vacancy.objects.all().exclude(VacancyId__in = vacancyList)

        self.assertEqual(response.status_code, 200)
        self.assertEqual((response.data['numVacancies']), len(vacancySet))