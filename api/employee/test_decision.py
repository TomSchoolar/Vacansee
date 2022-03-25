from django.test import TestCase
from employee.models import Favourite, Application, Reject
from employee.serializers import FavouriteSerializer, ApplicationSerializer, RejectSerializer

class decisionTestCase(TestCase):

    fixtures = ['authentication/fixtures/testseed.json']

    def test_favouriting(self):

        userid = 1
        vacancyid = 1

        response = self.client.post('/vacancy/fav/', { "UserId":userid, "VacancyId":vacancyid })

        favouriteSet = Favourite.objects.filter(
            UserId__exact = userid,
            VacancyId__exact = vacancyid
        )

        self.assertEqual(response.status_code, 201)

        correct_responce = False

        for fav in favouriteSet:
            if fav.FavouriteId == response.data['FavouriteId']:
                correct_responce = True

        self.assertEqual(correct_responce, True)

    def test_apply(self):

        userid = 1
        vacancyid = 1

        response = self.client.post('/vacancy/apply/', { "UserId":userid, "VacancyId":vacancyid })

        applicaionSet = Application.objects.filter(
            UserId__exact = userid,
            VacancyId__exact = vacancyid
        )

        self.assertEqual(response.status_code, 201)

        correct_responce = False

        for app in applicaionSet:
            if app.ApplicationId == response.data['ApplicationId']:
                correct_responce = True

        self.assertEqual(correct_responce, True)

    def test_reject(self):

        userid = 1
        vacancyid = 1

        response = self.client.post('/vacancy/reject/', { "UserId":userid, "VacancyId":vacancyid })

        rejectSet = Reject.objects.filter(
            UserId__exact = userid,
            VacancyId__exact = vacancyid
        )

        self.assertEqual(response.status_code, 201)

        correct_responce = False

        for rej in rejectSet:
            if rej.RejectId == response.data['RejectId']:
                correct_responce = True

        self.assertEqual(correct_responce, True)
