from copy import copy
from rest_framework import status
from ..models import RefreshToken, User
from ..serializers import UserSerializer
from employer.models import EmployerDetails
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.exceptions import ValidationError
from ..helpers import jwt as jwtHelper, auth as authHelper
from django.contrib.auth.hashers import make_password, check_password
from employee.models import Profile



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
    
    try:
        # get user type specific details
        if(user['IsEmployer']):
            extraDetails = authHelper.getEmployerDetails(user['UserId'])
        else:
            extraDetails = authHelper.getEmployeeDetails(user['UserId'])
    except User.DoesNotExist:
        return Response(data={'code': 400, 'message': 'could not find user details' }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as err:
        print(err)
        return Response(data={'code': 500, 'message': 'Server error while finding user details' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    # check if a user has already set up their profile
    profileSetup = True

    try:
        profileObj = Profile.objects.get(UserId__exact = userObj.UserId)

    except Profile.DoesNotExist:
        # can be an employer or an employee without a profile
        if(user['IsEmployer']):
            # no redirection is needed for employer
            pass
        else:
            profileSetup = False

    try:
        # remove private fields from user object
        userData = copy(user)
        userData = { **userData, **extraDetails, 'HasProfileSetup': profileSetup}
        toRemove = ['UserId', 'Password', 'PasswordResetToken', 'PasswordResetExpiration']

        for key in toRemove:
            del userData[key]

        # generate auth tokens
        accessToken = jwtHelper.createAccessToken(user['UserId'])
        refreshToken = jwtHelper.createRefreshToken(user['UserId'])

        # save refresh token in the db
        jwtHelper.saveRefreshToken(newJwt = refreshToken)
    except Exception as err:
        print(err)
        return Response(data={'code': 500, 'message': 'Server error while generating login data' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # return auth tokens and user data
    responseData = {
        'userData': userData,
        'accessToken': accessToken,
        'refreshToken': refreshToken,
    }

    return Response(data=responseData, status=status.HTTP_200_OK)



@api_view(['POST'])
def postRegister(request):
    body = request.data       

    try:
        User.objects.get(Email__exact=body['email'])

        return Response(data={'code': 409, 'message': 'account already exists for given email'}, status=status.HTTP_409_CONFLICT)
    except KeyError as err:
        return Response(data={'code': 400, 'message': f'incomplete form data: { err }'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        # we expect this, means that the user does not exist
        pass
    except Exception as err:
        print(err)
        return Response(data={'code': 500, 'message': 'Server error while finding user account'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        newUser = User(Email = body['email'], Password = make_password(body['password']), IsEmployer = body['isEmployer'])

        newUser.full_clean()
        newUser.save()

        user = UserSerializer(newUser).data
        
        if body['isEmployer']:
            employerDetails = EmployerDetails(UserId = newUser, CompanyName = body['companyName'], PhoneNumber = body['phoneNumber'])
            employerDetails.full_clean()
            employerDetails.save()

    except KeyError as err:
        failure = Response(data={'code': 400, 'message': f'incomplete form data: { err }'}, status=status.HTTP_400_BAD_REQUEST)
    except ValidationError as err:
        failure = Response(data={'code': 400, 'message': f'invalid form data: { err }'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as err:
        print(err)
        failure = Response(data={'code': 500, 'message': 'Server error while creating user account'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    finally:
        if 'failure' in locals():
            try:
                if 'newUser' in locals():
                    newUser.delete()
            except:
                pass

            return failure

    try:
        # remove private fields from user object
        userData = copy(user)
        userData = { **userData }
        toRemove = ['UserId', 'Password', 'PasswordResetToken', 'PasswordResetExpiration']

        for key in toRemove:
            del userData[key]

        if body['isEmployer']:
            userData['CompanyName'] = employerDetails.CompanyName
            userData['PhoneNumber'] = employerDetails.PhoneNumber

        # generate auth tokens
        accessToken = jwtHelper.createAccessToken(newUser.UserId)
        refreshToken = jwtHelper.createRefreshToken(newUser.UserId)

        # save refresh token in the db
        jwtHelper.saveRefreshToken(newJwt = refreshToken)

    except Exception as err:
        print(err)
        return Response(data={'code': 500, 'message': 'Server error while generating login data' }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # return auth tokens and user data
    responseData = {
        'userData': userData,
        'accessToken': accessToken,
        'refreshToken': refreshToken,
    }

    return Response(responseData, status=status.HTTP_201_CREATED)



@api_view(['POST'])
def postLogout(request):
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

