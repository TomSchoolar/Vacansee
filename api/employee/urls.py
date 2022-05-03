from django.urls import path
from .views import applications, favourites, index, account, profile

urlpatterns = [
    path('vacancies/', index.getIndex),
    path('vacancies/favourite/<int:vacancyId>/', favourites.postFavourite),
    path('vacancies/unfavourite/<int:vacancyId>/', favourites.deleteFavourite),
    path('vacancies/apply/<int:vacancyId>/', applications.postApplication),
    path('vacancies/reject/<int:vacancyId>/', index.postReject),
    path('applications/', applications.getApplications),
    path('applications/stats/', applications.getApplicationStats),
    path('applications/delete/<int:applicationId>/', applications.deleteApplication),
    path('applications/<int:applicationId>/', applications.getApplicationDetails),
    path('favourites/', favourites.getFavourites),
    path('accounts/', account.getAccount),
    path('accounts/update/', account.putAccount),
    path('accounts/delete/', account.deleteAccount),
    path('accounts/profiles/', account.getProfile),
    path('profiles/', profile.postProfile)
]
