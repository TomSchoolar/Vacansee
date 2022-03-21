import environ
import regex as re
import jwt as jwtLib
from employer.models import Vacancy
from authentication.models import User
from employee.models import Application, Profile
from employer.serializers import VacancySerializer
from authentication.serializers import UserEmailSerializer
from employee.serializers import ApplicationSerializer, ProfileSerializer, SummaryProfileSerializer


env = environ.Env()


def extractJwt(request):
    # get jwt from request

    authToken = request.META.get('HTTP_AUTHORIZATION')
    authTokenRegex = re.compile(r'^Bearer: (.+\..+\..+)')

    jwtRegex = authTokenRegex.match(authToken)
    jwt = jwtRegex.group(1)

    jwt = jwtLib.decode(jwt, env('JWT_SECRET'), algorithms=['HS256'])

    return jwt



def checkUserOwnsVacancy(vacancyId, jwt):
    # check the user that made the request owns the vacancy that they are requesting the data for

    userId = jwt['id']

    vacancySet = Vacancy.objects.get(pk = vacancyId, UserId__exact = userId)
    vacancySerializer = VacancySerializer(vacancySet)
    vacancy = vacancySerializer.data

    if not vacancy:
        return False
    return vacancy



def getApplications(vacancyId):
    # get the matches and pending applications for review page

    matchesSet = Application.objects.filter(
        VacancyId__exact = vacancyId,
        ApplicationStatus__exact = 'MATCHED'
    )

    newSet = Application.objects.filter(VacancyId__exact = vacancyId, ApplicationStatus__exact = 'PENDING')
    new = ApplicationSerializer(newSet, many = True).data
    populatedNew = pairApplications(new, ProfileSerializer)

    matchesSet = Application.objects.filter(VacancyId__exact = vacancyId, ApplicationStatus__exact = 'MATCHED')
    matches = ApplicationSerializer(matchesSet, many = True).data
    populatedMatches = pairApplications(matches, SummaryProfileSerializer)

    newSet = Application.objects.filter(
        VacancyId__exact = vacancyId,
        ApplicationStatus__exact = 'PENDING'
    )[:1]

    newSerializer = ApplicationSerializer(newSet, many = True)
    new = newSerializer.data

    # pair new applications with user profile
    populatedNew = pairApplications(new, ProfileSerializer)

    return { 'matches': populatedMatches, 'new': populatedNew }



def pairApplications(applications, serializer):
    # pair matches with user profile

    pairedApplications = []

    for app in applications:
        profileSet = Profile.objects.get(UserId__exact = app['UserId'])
        profile = serializer(profileSet).data

        if serializer == SummaryProfileSerializer:
            userSet = User.objects.get(pk = app['UserId'])
            user = UserEmailSerializer(userSet).data
            profile['Email'] = user['Email']

        pairedApplications.append({ 'application': app, 'profile': profile })

    return pairedApplications
