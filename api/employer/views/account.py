from rest_framework import status
from ..models import EmployerDetails
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..serializers import EmployerDetailsSerializer
from authentication.helpers import jwt as jwtHelper
from employer.helpers import getAccount as accountHelper



@api_view(['GET', 'PUT', 'DELETE'])
def getAccount(request):
    # get jwt
    
    jwt = jwtHelper.extractJwt(request)

    if type(jwt) is not dict:
        return jwt

    if request.method == 'PUT':
        return putAccount(request, jwt)
    elif request.method == 'DELETE':
        return deleteAccount(request, jwt)

    try:
        detailsSet = EmployerDetails.objects.get(UserId__exact=jwt['id'])
        detailsSerializer = EmployerDetailsSerializer(detailsSet)
        details = detailsSerializer.data

    except Exception as err:
        print(f'uh oh: { err }')
        return Response(data={ 'status': 500, 'message': 'Error acquiring details'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        email = accountHelper.getEmail(jwt['id'])

    except Exception as err:
        print(f'uh oh: { err }')
        return Response(data={ 'status': 500, 'message': 'Error acquiring email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    returnData = {
        'details': details,
        'email': email['Email']
    }

    return Response(returnData)



def putAccount(request, jwt):
    # destructure
    try:
        newCompanyName = request.data['setCompanyName']
        newPhoneNumber = request.data['setPhoneNumber']
        newEmail = request.data['setEmail']
    except:
        return Response(data={'status': 400, 'message': 'incomplete request data'}, status=status.HTTP_400_BAD_REQUEST)

    # update EmployerDetails
    try:
        employerDetails = EmployerDetails.objects.get(UserId__exact=jwt['id'])
        employerDetails.CompanyName = newCompanyName
        employerDetails.PhoneNumber = newPhoneNumber
        employerDetails.save()
    except Exception as err:
        print(f'uh oh: { err }')
        return Response(data={'status': 500, 'message': 'server error updating details'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # update Email/User['Email']
    try:
        accountHelper.updateEmail(jwt['id'], newEmail)
    except Exception as err:
        print(f'uh oh: { err }')
        return Response(data={'status': 500, 'message': 'server error updating email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({ 'status': 200, 'message': 'Account updated.'}, status=status.HTTP_200_OK)


def deleteAccount(request, jwt):
    try:
        accountHelper.deleteUser(jwt['id'])
        return Response(status=status.HTTP_200_OK)

    except Exception as err:
        print(f'uh oh: { err }')
        return Response(data={'status':500, 'message':'Server error while finding and deleting account'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
