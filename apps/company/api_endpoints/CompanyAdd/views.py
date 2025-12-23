from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView

from apps.company.models import ProductConfig
from .serializers import CompanyProductConfigSerializer


class CompanyCreateAPIView(CreateAPIView):
    queryset = ProductConfig.objects.all()
    serializer_class = CompanyProductConfigSerializer
    permission_classes = [IsAuthenticated, ]



__all__ = [
    "CompanyCreateAPIView"
]