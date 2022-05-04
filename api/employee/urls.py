from django.urls import path
from .views import applications, favourites, index, account, profile

urlpatterns = [
    path('vacancies/', index.getIndex),
    path('vacancies/<int:vacancyId>/favourite/', favourites.postFavourite),
    path('vacancies/<int:vacancyId>/unfavourite/', favourites.deleteFavourite),
    path('vacancies/<int:vacancyId>/apply/', applications.postApplication),
    path('vacancies/<int:vacancyId>/reject/', index.postReject),
    path('applications/', applications.getApplications),
    path('applications/stats/', applications.getApplicationStats),
    path('applications/<int:applicationId>/', applications.getApplicationDetails),
    path('favourites/', favourites.getFavourites),
    path('accounts/', account.getAccount),
    path('accounts/', account.putAccount),
    path('accounts/', account.deleteAccount),
    path('accounts/profiles/', account.getProfile),
    path('profiles/', profile.postProfile)
]
