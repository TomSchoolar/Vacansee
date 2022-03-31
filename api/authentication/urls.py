from . import views
from django.urls import path

urlpatterns = [
    path('login/', views.postLogin),
    path('logout/', views.getLogout)
]