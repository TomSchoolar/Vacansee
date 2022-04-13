from authentication.serializers import UserSerializer
from authentication.models import User
from employer.serializers import EmployerDetailsSerializer
from employer.models import EmployerDetails

def getEmail(userId):
    emailSet = User.objects.get(UserId=userId)
    email = UserSerializer(emailSet).data

    return email

def updateEmail(userId, newEmail):
    user = User.objects.get(UserId=userId)
    user.Email = newEmail
    user.save()

    return

def deleteUser(userId):
    user = User.objects.get(UserId=userId)
    user.delete()

    return