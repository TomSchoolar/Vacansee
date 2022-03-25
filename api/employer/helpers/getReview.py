import environ
import regex as re
import jwt as jwtLib
from employer.models import Vacancy
from authentication.models import User
from employee.models import Application, Profile
from employer.serializers import VacancySerializer
from employee.serializers import ApplicationSerializer, ProfileSerializer, SummaryProfileSerializer


env = environ.Env()


def checkUserOwnsVacancy(vacancyId, jwt):
    # check the user that made the request owns the vacancy that they are requesting the data for

    userId = jwt['id']

    vacancySet = Vacancy.objects.get(pk = vacancyId, UserId__exact = userId)
    vacancySerializer = VacancySerializer(vacancySet)
    vacancy = vacancySerializer.data

    return vacancy



def getNewApplication(vacancyId):
    newSet = Application.objects.filter(
        VacancyId__exact = vacancyId, 
        ApplicationStatus__exact = 'PENDING'
    ).order_by(
        'LastUpdated'
    )[:1]

    if len(newSet):
        new = ApplicationSerializer(newSet, many = True).data
        populatedNew = pairApplications(new, ProfileSerializer)
        return populatedNew[0]
    return False



def getApplications(vacancyId):
    # get the matches and pending applications for review page

    matchesSet = Application.objects.filter(
        VacancyId__exact = vacancyId,
        ApplicationStatus__exact = 'MATCHED'
    )

    matchesSet = Application.objects.filter(VacancyId__exact = vacancyId, ApplicationStatus__exact = 'MATCHED')
    matches = ApplicationSerializer(matchesSet, many = True).data
    populatedMatches = pairApplications(matches, SummaryProfileSerializer)

    populatedNew = getNewApplication(vacancyId)

    if populatedNew:
        return { 'matches': populatedMatches, 'new': populatedNew }
    return { 'matches': populatedMatches }



def pairApplications(applications, serializer):
    # pair matches with user profile

    pairedApplications = []

    for app in applications:
        profileSet = Profile.objects.get(UserId__exact = app['UserId'])
        profile = serializer(profileSet).data

        if serializer == SummaryProfileSerializer:
            user = User.objects.get(pk = app['UserId'])
            profile['Email'] = user.Email

        pairedApplications.append({ 'application': app, 'profile': profile })

    return pairedApplications
