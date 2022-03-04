import imp
from telnetlib import AUTHENTICATION
from time import timezone
from django.db import models
from django.apps import apps
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Profile(models.Model):
    UserId = models.ForeignKey('authentication.User', on_delete=models.PROTECT)
    FirstName = models.CharField(max_length=50, default="FirstName")
    LastName = models.CharField(max_length=50, default="LastName")
    Pronouns = models.CharField(max_length=50, default="")
    TimeZone = models.IntegerField(default=0)
    TopicSentence = models.CharField(max_length=500, default="")
    NotableSkills = ArrayField(models.CharField(max_length=500), size=3, default=list)
    #Experience
    Qualifications = ArrayField(models.CharField(max_length=500), size=3, default=list)
    PhoneNumber = models.CharField(max_length=11, default="00000000000")

class Favourite(models.Model):
    FavouriteId = models.AutoField(primary_key=True)
    UserId = models.ForeignKey('authentication.User', on_delete=models.PROTECT, default=0)
    VacancyId = models.ForeignKey('employer.Vacancy', on_delete=models.PROTECT, default=0)

class Application(models.Model):

    class ApplicationStatusValues(models.TextChoices):
        MATCHED = "MATCHED"
        REJECTED = "REJECTED"
        PENDING = "PENDING"

    ApplicationId = models.AutoField(primary_key=True)
    UserId = models.ForeignKey('authentication.User', blank=False, on_delete=models.PROTECT)
    VacancyId = models.ForeignKey('employer.Vacancy', blank=False, on_delete=models.PROTECT)
    ApplicationStatus = models.CharField(max_length=20, 
    choices=ApplicationStatusValues.choices,
    default=ApplicationStatusValues.PENDING)