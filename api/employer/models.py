import imp
from telnetlib import AUTHENTICATION
from django.utils import timezone
from django.db import models
from django.apps import apps
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class EmployerDetails(models.Model):
    UserId = models.OneToOneField('authentication.User', on_delete=models.CASCADE, primary_key=True)
    PhoneNumber = models.CharField(max_length=30)
    CompanyName = models.CharField(max_length=30)

class Vacancy(models.Model):
    class Meta:
        ordering = ('VacancyName', 'Created')

    VacancyId = models.AutoField(primary_key=True)
    VacancyName = models.CharField(max_length=80)
    UserId = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    Salary = models.CharField(max_length=80)
    Description = models.CharField(max_length=150)
    SkillsRequired = ArrayField(models.CharField(max_length=50), size=3, default=list, blank=True)
    ExperienceRequired = ArrayField(models.CharField(max_length=75), size=3, default=list, blank=True)
    TimeZone = models.IntegerField(blank=False)
    Tags = ArrayField(models.IntegerField(), size=10, default=list, blank=True)
    IsOpen = models.BooleanField(default=True)
    PhoneNumber = models.CharField(max_length=30)
    Email = models.EmailField(max_length=254)
    Created = models.DateTimeField(default=timezone.now)
    Location = models.CharField(max_length=30)


class Tag(models.Model):
    TagId = models.AutoField(primary_key=True)
    TagName = models.CharField(max_length=20)
    TagStyle = models.CharField(max_length=30, default='')


