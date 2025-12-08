from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.accounts.models import Employee
from .serializers import UpdateEmployeeSerializer


class EmployeeUpdateAPIView(UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = UpdateEmployeeSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"


    def get_queryset(self):
        return Employee.objects.filter(employer=self.request.user)