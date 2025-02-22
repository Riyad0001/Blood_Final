from django.urls import path
from .views import (
    UserRegistrationView,
    VerifyEmailView,
    UserLoginView,
    LogOutApiView,
    ProfileUpdateView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('verify-email/<str:uidb64>/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogOutApiView.as_view(), name='logout'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
]