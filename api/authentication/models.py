from django.db import models
from datetime import datetime, timezone, timedelta

def getAccessExpiry():
    # function to create date object extended to 10 mins from now
    return datetime.now(tz=timezone.utc) + timedelta(minutes=10)

# Create your models here.
class User(models.Model):
    UserId = models.AutoField(primary_key=True) 
    Email = models.EmailField(max_length=254, blank=False, unique=True)
    IsEmployer = models.BooleanField(default=False, blank=False)
    Password = models.CharField(max_length=100, blank=False)
    PasswordResetToken = models.CharField(max_length=100, null=True, blank=True)
    PasswordResetExpiration = models.DateTimeField(null=True, blank=True)


class RefreshToken(models.Model):
    TokenId = models.AutoField(primary_key=True)
    FamilyId = models.IntegerField(null=False)
    Token = models.CharField(max_length=200, null=False, unique=True)
    Expiry = models.DateTimeField(null=False, default=getAccessExpiry)
    IsLatest = models.BooleanField(null=False, default=True)