from rest_framework import status
from ..models import RefreshToken
from ..helpers import jwt as jwtHelper
from rest_framework.response import Response
from rest_framework.decorators import api_view



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