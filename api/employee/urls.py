from django.urls import path
from .views import applications, favourites, index, account, profile

urlpatterns = [
    path('vacancy/', index.getIndex),
    path('vacancy/fav/', favourites.postFavourite),
    path('vacancy/apply/', applications.postApplication),
    path('vacancy/reject/', index.postReject),
    path('applications/', applications.getApplications),
    path('applications/stats/', applications.getApplicationStats),
    path('applications/delete/<int:applicationId>/', applications.deleteApplication),
    path('applications/<int:applicationId>/', applications.getApplicationDetails),
    path('favourites/', favourites.getFavourites),
    path('account/', account.getAccount),
    path('account/update/', account.putAccount),
    path('account/delete/', account.deleteAccount),
    path('profile/', profile.postIndex)
]
