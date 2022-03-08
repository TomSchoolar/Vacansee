from datetime import datetime
from enum import Enum
import imp
from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class User(models.Model):
    UserId = models.AutoField(primary_key=True) 
    Email = models.EmailField(max_length=254, blank=False, unique=True)
    IsEmployer = models.BooleanField(default=False, blank=False)
    PasswordHash = models.CharField(max_length=500)
    PasswordSalt = models.CharField(max_length=500)
    PasswordResetToken = models.CharField(max_length=100, null=True)
    PasswordResetExpiration = models.DateField(null=True)