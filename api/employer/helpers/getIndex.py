from employer.models import Vacancy
from employee.models import Application
from employer.serializers import VacancySerializer


def getStats(uID):
    # returns top of page stats
    stats = {
        'activeAdverts': 0,
        'totalApplications': 0,
        'newApplications': 0,
        'acceptedApplications': 0,
        'rejectedApplications': 0,
    }

    vacanciesSet = Vacancy.objects.filter(UserId__exact = uID)
    vacancies = VacancySerializer(vacanciesSet, many=True).data

    for vacancy in vacancies:
        if vacancy['IsOpen']:
            stats['activeAdverts'] += 1

        new = Application.objects.filter(
            VacancyId__exact = vacancy['VacancyId'],
            ApplicationStatus__exact = 'PENDING'
        ).count()

        accepted = Application.objects.filter(
            VacancyId__exact = vacancy['VacancyId'],
            ApplicationStatus__exact = 'MATCHED'
        ).count()

        rejected = Application.objects.filter(
            VacancyId__exact = vacancy['VacancyId'],
            ApplicationStatus__exact = 'REJECTED'
        ).count()

        stats['newApplications'] += new
        stats['acceptedApplications'] += accepted
        stats['rejectedApplications'] += rejected
        stats['totalApplications'] += new + accepted + rejected

    return stats




def getVacancyStats(vacancies):
    # function to get number of accepted, rejected and pending applications

    for vacancy in vacancies:
        vacancy['NewApplications'] = Application.objects.filter(
            VacancyId__exact = vacancy['VacancyId'],
            ApplicationStatus__exact = 'PENDING'
        ).count()

        vacancy['AcceptedApplications'] = Application.objects.filter(
            VacancyId__exact = vacancy['VacancyId'],
            ApplicationStatus__exact = 'MATCHED'
        ).count()

        vacancy['RejectedApplications'] = Application.objects.filter(
            VacancyId__exact = vacancy['VacancyId'],
            ApplicationStatus__exact = 'REJECTED'
        ).count()
