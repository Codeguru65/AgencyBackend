from django.urls import path
from .views import RegisterView, LogoutAPIView, SetNewPasswordAPIView, VerifyEmail, \
    LoginAPIView, PasswordTokenCheckAPI,  DeleteUser, \
    GetUser, Welcome, RegisterInstitutionView, RequestPasswordResetEmail, UserView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('institution/', RegisterInstitutionView.as_view(), name="institution"),
    path('get-user/', GetUser.as_view(), name="get-user"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('welcome/', Welcome.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),
    path('delete/<int:id>', DeleteUser.as_view(), name='delete_user'),
    path('users/', UserView.as_view(), name='users')
]
