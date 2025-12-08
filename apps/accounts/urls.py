from django.urls import path

from apps.accounts.api_endpoints import (
    # User
    UserRegisterAPIView,
    UserLoginAPIView,
    VerifyCodeAPIView,
    UserGetUpdateProfileAPIView,
    UserLogoutView,
    # Employee
    CreateEmployeeAPIView,
)

app_name = "accounts"

urlpatterns = [
    # User
    path("register/", UserRegisterAPIView.as_view(), name="user-register"),
    path("login/", UserLoginAPIView.as_view(), name="user-login"),
    path("verify/code/", VerifyCodeAPIView.as_view(), name="user-verify-code"),
    path("profile/", UserGetUpdateProfileAPIView.as_view(), name="get-update-profile"),
    path("logout/", UserLogoutView.as_view(), name="user-logout"),
    # Employee
    path("employee/add/", CreateEmployeeAPIView.as_view(), name="employee-add")
]