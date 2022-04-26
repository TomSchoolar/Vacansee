from pydoc import plain
from secrets import token_urlsafe
from hashlib import sha256
from datetime import datetime, timezone, timedelta
from django.core.mail import send_mail
from django.conf import settings

def getResetExpiry():
    # function to create date object extended to 10 minutes from now
    return datetime.now(tz=timezone.utc) + timedelta(minutes=10)

def createResetPlainToken():
    plainToken = token_urlsafe(75)

    return plainToken

def createResetHashedToken(pt):
    hashedToken = sha256(pt.encode()).hexdigest()

    return hashedToken

def saveResetToken(token, user):
    expiry = getResetExpiry()
    user.PasswordResetToken = token
    user.PasswordResetExpiration = expiry.strftime('%Y-%m-%dT%H:%M:%S+0000')
    user.save(update_fields=['PasswordResetToken','PasswordResetExpiration'])

def checkExpiration(user):
    expiration = user.PasswordResetExpiration
    if (datetime.now(tz=timezone.utc) > expiration):
        return False
    else:
        return True

def sendEmail(token, email):
    url = 'http://tp45.co.uk/reset/{}'.format(token)

    #print('Sending mail...')

    email = send_mail(
        subject='Password Reset',
        message='You have requested a password reset - use the following URL to reset your password: {}'.format(url),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )

    if email == 1:
        #print('Email sent.')
        return True
    else:
        #print('Email failed to send.')
        return False
