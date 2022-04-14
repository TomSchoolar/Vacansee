from employee.serializers import ApplicationSerializer, ProfileSerializer, SummaryProfileSerializer
from employee.models import Application, Profile
from authentication.models import User
from employer.models import Vacancy

def getDetails(userId):
    
    profileSet = Profile.objects.filter(
        UserId__exact = userId
    )    

    profileSerializer = ProfileSerializer(profileSet, many=True)
    profile = profileSerializer.data

    return profile
