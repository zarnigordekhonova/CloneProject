from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .serializers import EmployeeAddSalarySerializer
from apps.accounts.models import EmployeePayment, Employee


class EmployeeAddSalaryAPIView(CreateAPIView):
    queryset = EmployeePayment.objects.all()
    serializer_class = EmployeeAddSalarySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        employee_id = self.request.data.get("employee")
        employee = Employee.objects.filter(id=employee_id).first()

        if employee.employer != self.request.user:
            raise PermissionDenied("You can add salary only to your employees.")
        
        serializer.save()



__all__ = [
    "EmployeeAddSalaryAPIView"
]