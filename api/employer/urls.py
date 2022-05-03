from django.urls import path
from .views import account, index, matches, review

urlpatterns = [
    path('vacancies/', index.getIndex),
    path('vacancies/stats/', index.getIndexStats),
    path('vacancies/close/<int:vacancyId>/', index.putIndexCloseVacancy),
    path('vacancies/delete/<int:vacancyId>/', index.deleteIndexDeleteVacancy),
    path('vacancies/edit/<int:vacancyId>/', index.editVacancy),
    path('reviews/<int:vacancyId>/', review.getReview),
    path('reviews/<int:vacancyId>/updatestatus/<int:applicationId>/', review.putReviewApplication),
    path('matches/', matches.getMatchVacancies),
    path('matches/matches/<int:vacancyId>/', matches.getMatches),
    path('matches/cards/<int:applicantId>/', matches.getCard),
    path('accounts/', account.getAccount),
    path('accounts/update/', account.putAccount),
    path('accounts/delete/', account.deleteAccount)
]