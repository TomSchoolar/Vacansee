from . import views
from django.urls import path

urlpatterns = [
    path('vacancy/', views.getIndex),
    path('vacancy/stats/', views.getIndexStats),
    path('review/<int:vacancyId>/', views.getReview)
]