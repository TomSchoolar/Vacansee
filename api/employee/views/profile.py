from django.forms import ValidationError
from rest_framework import status
from authentication.models import User
from rest_framework.response import Response
from ..models import Profile
from rest_framework.decorators import api_view
from authentication.helpers import jwt as jwtHelper

@api_view(['POST'])
def postProfile(request):
    jwt = jwtHelper.extractJwt(request)

    if type(jwt) is not dict:
        return jwt

    try:
        data = request.data
    except:
        return Response({ 'status': 400 }, status=status.HTTP_400_BAD_REQUEST)

    try:
        data['UserId'] = User.objects.get(pk = jwt['id'])

        newProfile = Profile(**data)
        newProfile.full_clean()
        newProfile.save()

        return Response({ 'status': 200 }, status=status.HTTP_200_OK)
    except ValidationError as err:
        return Response({ 'status': 400, 'message': str(err) }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as err:
        import traceback
        traceback.print_exc()
        print(f'uh oh: { err }')
        return Response({ 'status': 500, 'message': str(err) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)