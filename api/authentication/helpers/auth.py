from employee.models import Profile
from employer.models import EmployerDetails
from random import randint
from ..models import User


def getEmployeeDetails(userId):
    return {}


def getEmployerDetails(userId):
    details = EmployerDetails.objects.get(UserId__exact = userId)

    return {
        'CompanyName': details.CompanyName,
        'PhoneNumber': details.PhoneNumber
    }


def generateUserId(body):
    userId = randint(1,10000)

    try:
        userObj = User.objects.get(UserId__exact = userId)
        generateUserId(body)
    except User.DoesNotExist:
        return userId
    except Exception as err:
        print(err)
        generateUserId(body)

