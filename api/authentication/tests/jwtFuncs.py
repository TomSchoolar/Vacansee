import environ
import jwt as jwtLib
from datetime import datetime, timezone, timedelta


env = environ.Env()


def createJwt(uid, expire='later'):
    jwt = { 
        'id': uid,
        'exp': datetime.now(tz=timezone.utc) + timedelta(minutes=60),
        'iat': datetime.now(tz=timezone.utc),
        'typ': 'access'
    }

    if expire == 'now':
        jwt['exp'] = datetime.now(tz=timezone.utc) - timedelta(minutes=1)

    encodedJWT = jwtLib.encode(
        jwt,
        env('JWT_SECRET'),
        algorithm='HS256'
    )

    return encodedJWT