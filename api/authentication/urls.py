from django.urls import path
from .views import doorAuth, jwt, reset

urlpatterns = [
    path('login/', doorAuth.postLogin),
    path('logout/', doorAuth.postLogout),
    path('refreshtoken/', jwt.postRefreshToken),
    path('forgot/', reset.postEmail),
    path('reset/<str:token>/', reset.getReset),
    path('reset/', reset.postReset)
]