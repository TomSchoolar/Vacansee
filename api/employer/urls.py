from django.urls import path
from .views import account, index, match, review

urlpatterns = [
    path('vacancy/', index.getIndex),
    path('vacancy/stats/', index.getIndexStats),
    path('review/<int:vacancyId>/', review.getReview),
    path('review/<int:vacancyId>/updatestatus/<int:applicationId>/', review.putReviewApplication),
    path('match/', match.getMatchVacancies),
    path('match/matches/', match.getMatches),
    path('match/card/', match.getCard),
    path('account/', account.getAccount),
    path('account/update/', account.putAccount),
    path('account/delete/', account.deleteAccount)
]