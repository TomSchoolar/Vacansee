from . import views
from django.urls import path

urlpatterns = [
    path('vacancy/', views.getIndex),
    path('applications/', views.getApplications)
]