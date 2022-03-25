import environ
import regex as re
import jwt as jwtLib


env = environ.Env()



def extractJwt(request):
    # get jwt from request

    authToken = request.META.get('HTTP_AUTHORIZATION')
    authTokenRegex = re.compile(r'^Bearer: (.+\..+\..+)')

    jwtRegex = authTokenRegex.match(authToken)
    jwt = jwtRegex.group(1)

    jwt = jwtLib.decode(jwt, env('JWT_SECRET'), algorithms=['HS256'])

    return jwt