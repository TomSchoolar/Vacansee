from copy import copy
from xml import dom
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .helpers import jwt as jwtHelper, password as passwordHelper


@api_view(['POST'])
def postLogin(request):
    # get vacancies matching userid
    body = request.data

    if(not body or not body['email'] or not body['password']):
        return Response(data={'code': 400, 'message': 'incomplete form data'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        userObj = User.objects.get(Email__exact=body['email'])
        user = UserSerializer(userObj).data
    except User.DoesNotExist:
        return Response(data={'code': 401, 'message': 'invalid login details'}, status=status.HTTP_401_UNAUTHORIZED)
    except User.MultipleObjectsReturned:
        return Response(data={'code': 500, 'message': 'multiple users found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    if not passwordHelper.correctPassword(body['password'], user):
        return Response(data={'code': 401, 'message': 'invalid login details'}, status=status.HTTP_401_UNAUTHORIZED)
    
    userData = copy(user)
    toRemove = ['PasswordHash', 'PasswordSalt', 'PasswordResetToken', 'PasswordResetExpiration']

    for key in toRemove:
        del userData[key]

    accessToken = jwtHelper.createAccessToken(user['UserId'])
    refreshToken = jwtHelper.createRefreshToken(user['UserId'])

    jwtHelper.saveRefreshToken(newJwt = refreshToken)

    responseData = {
        'userData': userData,
        'accessToken': accessToken,
        'refreshToken': refreshToken
    }

    return Response(data=responseData, status=status.HTTP_200_OK)



@api_view(['GET'])
def getLogout(request):

    jwt = jwtHelper.extractJwt(request)

    if type(jwt) is not dict:
        return jwt

    