import environ
import regex as re
import jwt as jwtLib
from rest_framework import status
from rest_framework.response import Response
from authentication.models import RefreshToken
from datetime import datetime, timezone, timedelta
from authentication.serializers import RefreshTokenSerializer


env = environ.Env()


def getRefreshExpiry():
    # function to create date object extended to 1 week from now
    return datetime.now(tz=timezone.utc) + timedelta(weeks=1)



def getAccessExpiry():
    # function to create date object extended to 10 mins from now
    return datetime.now(tz=timezone.utc) + timedelta(minutes=10)



def createAccessToken(userId):
    # function to return encoded and signed access jwt
    encodedJwt = jwtLib.encode(
        { 
            'id': userId,
            'exp': getAccessExpiry(),
            'iat': datetime.now(tz=timezone.utc),
            'typ': 'access'
        },
        env('JWT_SECRET'),
        algorithm='HS256'
    )

    return encodedJwt



def createRefreshToken(userId):
    # function to return encoded and signed refresh jwt
    encodedJwt = jwtLib.encode(
        { 
            'id': userId,
            'exp': getRefreshExpiry(),
            'iat': datetime.now(tz=timezone.utc),
            'typ': 'refresh'
        },
        env('JWT_SECRET'),
        algorithm='HS256'
    )

    return encodedJwt



def saveRefreshToken(newJwt, oldJwt = False):
    # function to create new token object in db and if necessary deactivate previous token
    if oldJwt:
        oldToken = RefreshToken.objects.get(Token__exact=oldJwt)
        oldToken.IsLatest = False
        oldToken.save()
    
        family = oldToken.FamilyId
    
    else:
        highestIdSet = RefreshToken.objects.all().order_by('FamilyId').last()

        if not highestIdSet:
            family = 0
        else:
            family = highestIdSet.FamilyId + 1

    expiry = jwtLib.decode(newJwt, env('JWT_SECRET'), algorithms=['HS256'])['exp']
        
    newToken = {
        'FamilyId': family,
        'Token': newJwt,
        'Expiry': expiry,
        'IsLatest': True
    }

    newTokenObj = RefreshToken(
        FamilyId = family,
        Token = newJwt,
        Expiry = datetime.fromtimestamp(expiry).strftime('%Y-%m-%dT%H:%M:%S+0000'),
        IsLatest = True
    )

    newTokenObj.save()



def extractJwt(request):
    # get jwt from request

    try:
        authToken = request.META.get('HTTP_AUTHORIZATION')
        authTokenRegex = re.compile(r'^Bearer: (.+\..+\..+)')

        jwtRegex = authTokenRegex.match(authToken)
        jwt = jwtRegex.group(1)

        jwt = jwtLib.decode(jwt, env('JWT_SECRET'), algorithms=['HS256'])

        return jwt
    except jwtLib.ExpiredSignatureError:
        return Response({ 'status': 401, 'message': 'Expired auth token' }, status=status.HTTP_401_UNAUTHORIZED)
    except (jwtLib.InvalidKeyError, jwtLib.InvalidSignatureError, jwtLib.InvalidTokenError) as err:
        return Response({ 'status': 401, 'message': 'Invalid auth token' }, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as err:
        print(f'uh oh: { err }')
        return Response({ 'status': 500, 'message': 'Error acquiring auth token' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)