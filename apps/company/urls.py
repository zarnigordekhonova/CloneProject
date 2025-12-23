from django.urls import path

from apps.company.api_endpoints import (
    CompanyCreateAPIView,
    CompanyUpdateAPIView,
)

app_name = "company"


urlpatterns = [
    path("add/", CompanyCreateAPIView.as_view(), name="company-add"),
    path("update/<int:pk>/", CompanyUpdateAPIView.as_view(), name="company-update"),
]