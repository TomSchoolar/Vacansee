from django.urls import path
from .views import account, index, matches, review

urlpatterns = [
    path('vacancies/', index.getIndex),
    path('vacancies/stats/', index.getIndexStats),
    path('vacancies/<int:vacancyId>/close/', index.putIndexCloseVacancy),
    path('vacancies/<int:vacancyId>/edit/', index.editVacancy),
    path('vacancies/<int:vacancyId>/', index.editVacancy),
    path('vacancies/<int:vacancyId>/review/', review.getReview),
    path('vacancies/<int:vacancyId>/review/<int:applicationId>/', review.putReviewApplication),
    path('matches/', matches.getMatchVacancies),
    path('matches/<int:vacancyId>/', matches.getMatches),
    path('matches/card/<int:applicantId>/', matches.getCard),
    path('accounts/', account.getAccount),
]