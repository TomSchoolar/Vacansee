from django.urls import path
from .views import doorAuth, jwt

urlpatterns = [
    path('login/', doorAuth.postLogin),
    path('logout/', doorAuth.postLogout),
    path('refreshtoken/', jwt.postRefreshToken)
]