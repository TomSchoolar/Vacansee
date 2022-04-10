from copy import copy
from rest_framework import status
from .models import RefreshToken, User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import check_password
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
    except Exception as err:
        print(err)
        return Response(data={'code': 500, 'message': 'Server error while finding user account'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # check if submitted password matches saved one
    if not check_password(body['password'], user['Password']):
        return Response(data={'code': 401, 'message': 'invalid login details'}, status=status.HTTP_401_UNAUTHORIZED)
    
    # remove private fields from user object
    userData = copy(user)
    toRemove = ['UserId', 'Password', 'PasswordResetToken', 'PasswordResetExpiration']

    for key in toRemove:
        del userData[key]

    # generate auth tokens
    accessToken = jwtHelper.createAccessToken(user['UserId'])
    refreshToken = jwtHelper.createRefreshToken(user['UserId'])

    # save refresh token in the db
    jwtHelper.saveRefreshToken(newJwt = refreshToken)

    # return auth tokens and user data
    responseData = {
        'userData': userData,
        'accessToken': accessToken,
        'refreshToken': refreshToken
    }

    return Response(data=responseData, status=status.HTTP_200_OK)



@api_view(['POST'])
def getLogout(request):
    # make sure refresh token has been provided and decode
    jwt = jwtHelper.extractExpiredJwt(request)

    if type(jwt) is not dict:
        return jwt

    # find and remove refresh token and all refresh tokens in family
    try:
        jwtHelper.destroyRefreshFamily(request)
    except RefreshToken.DoesNotExist as err:
        # refresh token in logout request doesn't exist
        pass
    except Exception as err:
        print(f'uh oh { err }')
        return Response({ 'status': 500, 'message': 'Server error while trying to delete refresh tokens'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status=status.HTTP_200_OK)
    

    
@api_view(['POST'])
def postRefreshToken(request):
    # get refresh token
    refreshToken = jwtHelper.extractJwt(request)

    if type(refreshToken) is not dict:
        return refreshToken

    try:
        refreshTokenString = jwtHelper.getTokenFromRequest(request)
    except Exception as err:
        print(f'strange error in token refresh request while getting refreshToken string from request')
        return Response({ 'status': 500, 'message': 'Server error while retrieving refresh token from request'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # find refresh token in db
    try: 
        token = RefreshToken.objects.get(Token__exact = refreshTokenString)

        if not token.IsLatest:
            # token reuse, delete whole family
            jwtHelper.destroyRefreshFamily(request)
            return Response({ 'status': 403, 'message': 'Token reuse detected' }, status=status.HTTP_403_FORBIDDEN)

        # refresh token is valid, not expired and the latest in its family
        newAccessToken = jwtHelper.createAccessToken(refreshToken['id'])
        newRefreshToken = jwtHelper.createRefreshToken(refreshToken['id'])

        jwtHelper.saveRefreshToken(newRefreshToken, refreshTokenString)

        return Response({ 'accessToken': newAccessToken, 'refreshToken': newRefreshToken }, status=status.HTTP_200_OK)

    except RefreshToken.DoesNotExist as err:
        return Response({ 'status': 401, 'message': 'provided refresh token is invalid' }, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as err:
        print(err)
        return Response({ 'status': 500, 'message': 'Server error while getting refresh token in access token refresh request'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

