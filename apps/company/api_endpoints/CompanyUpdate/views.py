from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView

from apps.company.models import Company
from .serializers import CompanyProductConfigUpdateSerializer


class CompanyUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyProductConfigUpdateSerializer
    permission_classes = [IsAuthenticated, ]
    lookup_field = "pk"



__all__ = [
    "CompanyUpdateAPIView"
]