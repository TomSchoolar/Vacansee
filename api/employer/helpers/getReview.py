from pstats import SortKey
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

def alphabeticalSort(applicationList, sortField):

    sortingDict = { }
    returnList = []

    for i in range(0, len(applicationList)):
        app = applicationList[i]
        sortingDict[app['profile'][sortField]] = i

    sortednames=sorted(sortingDict.keys(), key=lambda x:x.lower())

    counter = 0

    while len(sortingDict) > 0:
        returnList.append(applicationList[sortingDict[sortednames[0]]])
        sortingDict.pop(sortednames[0])
        sortednames.pop(0)

    return returnList


def getApplications(vacancyId, sortParam, searchValue):
    # get the matches and pending applications for review page

    profileLastSet = Profile.objects.filter(
        LastName__contains = searchValue
    )

    UserIdList = []

    for prof in profileLastSet:
        UserIdList.append(prof.UserId.UserId)

    totalCount = Application.objects.filter(
        VacancyId__exact = vacancyId,
        ApplicationStatus__exact = 'MATCHED'
    ).count()

    matchesSet = Application.objects.filter(
        VacancyId__exact = vacancyId,
        ApplicationStatus__exact = 'MATCHED',
        UserId__in = UserIdList
    )

    matches = ApplicationSerializer(matchesSet, many = True).data
    populatedMatches = pairApplications(matches, SummaryProfileSerializer)

    if sortParam == "FirstNameAsc" or sortParam == "FirstNameDesc":
        sortKey = "FirstName"
    else:
        sortKey = "LastName"

    populatedMatches = alphabeticalSort(populatedMatches, sortKey)

    if sortParam == 'FirstNameDesc' or sortParam == "LastNameDesc":
        newPopList = []

        for i in range(0, len(populatedMatches)):
            newPopList.append(populatedMatches[len(populatedMatches) - i - 1])

        populatedMatches = newPopList

    populatedNew = getNewApplication(vacancyId)

    if populatedNew:
        return { 'matches': populatedMatches, 'new': populatedNew, 'totalCount': totalCount }
    return { 'matches': populatedMatches, 'totalCount': totalCount }




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
