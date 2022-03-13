import jwt
import environ
from datetime import datetime, timezone, timedelta
from copy import copy
from .models import User
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

env = environ.Env()

@api_view(['POST'])
def postLogin(request):
    # get vacancies matching userid
    body = request.data

    if(not body or not body['email'] or not body['password']):
        return Response(data={'code': 400, 'message': 'incomplete form data'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        userObj = User.objects.get(Email__exact=body['email'])
    except User.DoesNotExist:
        return Response(data={'code': 401, 'message': 'invalid login details'}, status=status.HTTP_401_UNAUTHORIZED)
    except User.MultipleObjectsReturned:
        return Response(data={'code': 500, 'message': 'multiple users found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    user = UserSerializer(userObj).data
    
    if body['password'] != user['PasswordHash']:
        return Response(data={'code': 401, 'message': 'invalid login details'}, status=status.HTTP_401_UNAUTHORIZED)
    
    userData = copy(user)
    toRemove = ['PasswordHash', 'PasswordSalt', 'PasswordResetToken', 'PasswordResetExpiration']


    encodedJWT = jwt.encode(
        { 
            'id': userData['UserId'],
            'exp': datetime.now(tz=timezone.utc) + timedelta(minutes=10),
            'iat': datetime.now(tz=timezone.utc)
        },
        env('JWT_SECRET'),
        algorithm='HS256'
    )

    for key in toRemove:
        del userData[key]

    responseBody = {
        'userData': userData,
        'jwt': encodedJWT
    }

    return Response(data=responseBody, status=status.HTTP_200_OK)
