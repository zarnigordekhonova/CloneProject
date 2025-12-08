from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.accounts.models import Employee
from .serializers import CreateEmployeeSerializer


class CreateEmployeeAPIView(CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = CreateEmployeeSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user)


__all__ = [
    "CreateEmployeeAPIView"
]