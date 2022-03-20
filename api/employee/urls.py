from . import views
from django.urls import path

urlpatterns = [
    path('vacancy/fav/', views.postFavourite),
    path('vacancy/apply/', views.postApplication),
]