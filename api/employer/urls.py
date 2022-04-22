from django.urls import path
from .views import account, index, matches, review

urlpatterns = [
    path('vacancy/', index.getIndex),
    path('vacancy/stats/', index.getIndexStats),
    path('vacancy/edit/<int:vacancyId>/', index.editVacancy),
    path('review/<int:vacancyId>/', review.getReview),
    path('review/<int:vacancyId>/updatestatus/<int:applicationId>/', review.putReviewApplication),
    path('match/', matches.getMatchVacancies),
    path('match/matches/', matches.getMatches),
    path('match/card/', matches.getCard),
    path('account/', account.getAccount),
    path('account/update/', account.putAccount),
    path('account/delete/', account.deleteAccount)
]