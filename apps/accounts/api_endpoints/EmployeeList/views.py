from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.accounts.models import Employee
from .serializers import EmployeeListSerializer


class EmployeesListAPIView(ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Employee.objects.filter(employer=self.request.user).order_by("-created_at")
    


__all__ = [
    "EmployeesListAPIView"
]
