# Generated by Django 4.0.2 on 2022-03-15 22:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employer', '0003_alter_employerdetails_phonenumber_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vacancy',
            options={'ordering': ('VacancyName', 'Created')},
        ),
    ]