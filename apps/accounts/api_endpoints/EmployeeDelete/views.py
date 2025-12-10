from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.accounts.models import Employee


class EmployeeDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    lookup_url_kwarg = "employee_id"

    def get_queryset(self):
        return Employee.objects.filter(employer=self.request.user)
    

__all__ = [
    "EmployeeDeleteAPIView"
]
    