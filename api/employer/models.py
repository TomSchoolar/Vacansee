import imp
from telnetlib import AUTHENTICATION
from time import timezone
from django.db import models
from django.apps import apps
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class EmployerDetails(models.Model):
    UserId = models.OneToOneField('authentication.User', on_delete=models.CASCADE, primary_key=True, blank=False)
    PhoneNumber = models.CharField(max_length=30, blank=False)
    CompanyName = models.CharField(max_length=30, blank=False)

class Vacancy(models.Model):
    class Meta:
        ordering = ('VacancyName', 'Created')

    VacancyId = models.AutoField(primary_key=True)
    VacancyName = models.CharField(max_length=80, blank=False)
    UserId = models.ForeignKey('authentication.User', on_delete=models.CASCADE, blank=False)
    Salary = models.CharField(max_length=80, blank=False)
    Description = models.CharField(max_length=150, blank=False)
    SkillsRequired = ArrayField(models.CharField(max_length=50), size=3, default=list)
    ExperienceRequired = ArrayField(models.CharField(max_length=75), size=3, default=list)
    TimeZone = models.IntegerField(blank=False)
    Tags = ArrayField(models.CharField(max_length=20), size=10, default=list)
    IsOpen = models.BooleanField(blank=False, default=True)
    PhoneNumber = models.CharField(max_length=30, blank=False)
    Email = models.EmailField(max_length=254, blank=False)
    Created = models.DateField(auto_now_add=True, blank=False)
    Location = models.CharField(max_length=30, default="")


class Tag(models.Model):
    TagId = models.AutoField(primary_key=True)
    TagName = models.CharField(max_length=20, blank=False)


