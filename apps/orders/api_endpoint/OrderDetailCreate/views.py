from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from  apps.orders.models import OrderDetail
from .serializers import OrderDetailCreateSerializer


class OrderDetailCreateAPIView(CreateAPIView):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailCreateSerializer
    permission_classes = [IsAuthenticated, ]



__all__ = [
    "OrderDetailCreateAPIView"
]
