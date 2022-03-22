from . import views
from django.urls import path

urlpatterns = [
    path('vacancy/apply/', views.postApplication),
    path('vacancy/reject/', views.postReject),
    path('vacancy/fav/', views.postFavourite)
]