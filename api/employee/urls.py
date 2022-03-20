from . import views
from django.urls import path

urlpatterns = [
    path('vacancy/', views.getIndex),
    path('vacancy/fav/', views.postFavourite),
    path('vacancy/apply/', views.postApplication),
    path('applications/', views.getApplications),
    path('applications/stats/', views.getApplicationStats)
]