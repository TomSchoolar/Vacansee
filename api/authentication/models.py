from datetime import datetime
from enum import Enum
import imp
from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class User(models.Model):
    UserId = models.AutoField(primary_key=True, default=0) 
    Email = models.CharField(max_length=500, default="Default Email")
    IsEmployer = models.BooleanField(default=False, blank=False)
    PasswordHash = models.CharField(max_length=500, default="Hash")
    PasswordSalt = models.CharField(max_length=500, default="Salt")
    PasswordResetToken = models.CharField(max_length=500, default="Token")
    PasswordResetExpiration = models.DateField(default=datetime.now)