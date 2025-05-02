from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . views import RegisterView, LoginView
urlpatterns = [
    path('register/', RegisterView.as_view() , name= "auth_register"),
    path('login/', LoginView.as_view() , name= "auth_login"),
    path('<str:group_name>/', views.index),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
