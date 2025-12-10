from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .serializers import EmployeeSerializer, EmployeeSalariesListSerializer
from apps.accounts.models import Employee, EmployeePayment


class EmployeeSalariesHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    lookup_field = "employee_id"

    def get(self, request, *args, **kwargs):
        employee = Employee.objects.get(id=self.kwargs["employee_id"])

        if employee.employer != self.request.user:
            raise PermissionDenied("You can view only your employee's salary history.")
        
        employee_data = EmployeeSerializer(employee)
        salary_data = EmployeePayment.objects.filter(employee=employee).order_by("-created_at")
        salary_history = EmployeeSalariesListSerializer(salary_data, many=True)

        return Response(
            {"user_data" : employee_data.data,
             "salary_history" : salary_history.data},
             status=status.HTTP_200_OK
        )
        


__all__ = [
    "EmployeeSalariesHistoryAPIView"
]