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
    EmployeesListAPIView,
    EmployeeUpdateAPIView,
    EmployeeAddSalaryAPIView,
    EmployeeSalariesHistoryAPIView,
    EmployeeDeleteAPIView,
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
    path("employee/add/", CreateEmployeeAPIView.as_view(), name="employee-add"),
    path("employees/list/", EmployeesListAPIView.as_view(), name="employees-list"),
    path("employee/<int:pk>/update/", EmployeeUpdateAPIView.as_view(), name="employee-update"),
    path("employee/salary/", EmployeeAddSalaryAPIView.as_view(), name="employee-add-salary"),
    path("employee/<int:employee_id>/salaries/history/", 
         EmployeeSalariesHistoryAPIView.as_view(),
         name="employee-salaries-history"),
    path("employee/<int:employee_id>/delete/", EmployeeDeleteAPIView.as_view(), name="employee-delete   ")
    
    
]