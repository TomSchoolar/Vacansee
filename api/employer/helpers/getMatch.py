from employee.serializers import ApplicationSerializer, ProfileSerializer, SummaryProfileSerializer
from employee.models import Application, Profile
from authentication.models import User
from employer.models import Vacancy


def getMatchesOTHER(vacancyId):

    matchesSet = Application.objects.filter(
        VacancyId__exact = vacancyId,
        ApplicationStatus__exact = 'MATCHED'
    )

    numMatches = Application.objects.filter(
        VacancyId__exact = vacancyId,
        ApplicationStatus__exact = 'MATCHED'
    ).count()

    matchesSerializer = ApplicationSerializer(matchesSet, many = True)
    matches = matchesSerializer.data


    return { 'matches': matches, 'numMatches': numMatches}

def getDetails(userId):
    
    profileSet = Profile.objects.filter(
        UserId__exact = userId
    )    

    profileSerializer = ProfileSerializer(profileSet, many=True)
    profile = profileSerializer.data

    return profile

def getMatches(vacancyId):
    # get the matches and pending applications for review page

    numMatches = Application.objects.filter(
        VacancyId__exact = vacancyId,
        ApplicationStatus__exact = 'MATCHED'
    ).count()

    matchesSet = Application.objects.filter(VacancyId__exact = vacancyId, ApplicationStatus__exact = 'MATCHED')
    matches = ApplicationSerializer(matchesSet, many = True).data
    populatedMatches = pairMatches(matches, SummaryProfileSerializer)

    return { 'matches': populatedMatches, 'numMatches': numMatches }

def pairMatches(matches, serializer):
    # pair matches with user profile

    pairedMatches = []

    for match in matches:
        profileSet = Profile.objects.get(UserId__exact = match['UserId'])
        profile = serializer(profileSet).data

        if serializer == SummaryProfileSerializer:
            user = User.objects.get(pk = match['UserId'])
            profile['Email'] = user.Email

        pairedMatches.append({ 'application': match, 'profile': profile })

    return pairedMatches
