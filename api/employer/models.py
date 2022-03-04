import imp
from telnetlib import AUTHENTICATION
from time import timezone
from django.db import models
from django.apps import apps
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class EmployerDetails(models.Model):
    UserId = models.ForeignKey('authentication.User', on_delete=models.PROTECT)
    PhoneNumber = models.CharField(max_length=11, default="00000000000")
    CompanyName = models.CharField(max_length=30, default="Company Name")

class Vacancy(models.Model):
    VacancyId = models.AutoField(primary_key=True)
    VacancyName = models.CharField(max_length=500, blank=False, default="Name")
    UserId = models.ForeignKey('authentication.User', on_delete=models.PROTECT, default=0)
    Salary = models.CharField(max_length=500, blank=False, default="Competitive")
    Description = models.CharField(max_length=500, default="Description")
    SkillsRequired = ArrayField(models.CharField(max_length=500), size=3, default=list)
    ExperienceRequired = ArrayField(models.CharField(max_length=500), size=3, default=list)
    TimeZone = models.IntegerField(blank=False, default=0)
    Tags = ArrayField(models.CharField(max_length=10), size=10, default=list)
    IsOpen = models.BooleanField(blank=False, default=True)
    PhoneNumber = models.CharField(max_length=11, blank=False, default="00000000000")
    Email = models.CharField(max_length=500, blank=False, default="user@tindeed.com")



class Tag(models.Model):
    TagId = models.AutoField(primary_key=True)
    TagName = models.CharField(max_length=500, blank=False, default="Name")


