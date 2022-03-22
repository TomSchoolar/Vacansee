import imp
from telnetlib import AUTHENTICATION
from time import timezone
from django.db import models
from django.apps import apps
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Profile(models.Model):
    UserId = models.OneToOneField('authentication.User', on_delete=models.CASCADE, primary_key=True, blank=False)
    FirstName = models.CharField(max_length=50, blank=False)
    LastName = models.CharField(max_length=50, blank=False)
    Pronouns = models.CharField(max_length=50)
    TimeZone = models.IntegerField(blank=False)
    TopicSentence = models.CharField(max_length=200, default="")
    NotableSkills = ArrayField(models.CharField(max_length=50), size=3, default=list)
    Experience = ArrayField(models.CharField(max_length=80), size=3, default=list)
    Qualifications = ArrayField(models.CharField(max_length=80), size=3, default=list)
    PhoneNumber = models.CharField(max_length=30, blank=False)

class Favourite(models.Model):
    FavouriteId = models.AutoField(primary_key=True)
    UserId = models.ForeignKey('authentication.User', on_delete=models.CASCADE, blank=False)
    VacancyId = models.ForeignKey('employer.Vacancy', on_delete=models.CASCADE, blank=False)

class Application(models.Model):

    class ApplicationStatusValues(models.TextChoices):
        MATCHED = "MATCHED"
        REJECTED = "REJECTED"
        PENDING = "PENDING"

    ApplicationId = models.AutoField(primary_key=True)
    UserId = models.ForeignKey('authentication.User', blank=False, on_delete=models.CASCADE)
    VacancyId = models.ForeignKey('employer.Vacancy', blank=False, on_delete=models.CASCADE)
    ApplicationStatus = models.CharField(
        max_length=20,
        blank=False,
        choices=ApplicationStatusValues.choices,
        default=ApplicationStatusValues.PENDING
    )

class Reject(models.Model):
    RejectId = models.AutoField(primary_key=True)
    UserId = models.ForeignKey('authentication.User', blank=False, on_delete=models.CASCADE)
    VacancyId = models.ForeignKey('employer.Vacancy', blank=False, on_delete=models.CASCADE)